import "bingmaps";
import { initialize, loadModule, whenLoaded, moduleNames } from "bing-maps-loader";
import { Component, OnInit } from '@angular/core';
import { WasteTypeControllerService } from './core/api/locate'
import { Classification } from './file-upload.component';
import { environment } from "src/environments/environment";

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss']
})
export class AppComponent implements OnInit {

  category: string = "";
  confidence: string = "";
  closestAddress: string = "";
  searchBox: string = "#searchBox";
  searchBoxContainer: string = "#searchBoxContainer";

  private map: any = null;
  private yourPin: any = null;
  private binPin: any = null;

  // Inject the generated Angular service as a dependency of this class
  constructor(private wasteTypeControllerService: WasteTypeControllerService) { }

  ngOnInit() {
    initialize(environment.bingApiKey);
    whenLoaded
      .then(() => loadModule(moduleNames.AutoSuggest))
      .then(() => {
        this.map = new Microsoft.Maps.Map("#map", { zoom: 15, enableCORS: true, enableHighDpi: true });

        const options: Microsoft.Maps.IAutosuggestOptions = {
          autoDetectLocation: true,
          countryCode: 'AT',
          maxResults: 3,
          placeSuggestions: true,
          map: this.map,
          useMapView: true
        };

        // Get the initial location from the browser geolocation
        if (navigator.geolocation) {
          navigator.geolocation.getCurrentPosition((position) => {
            const location = new Microsoft.Maps.Location(position.coords.latitude, position.coords.longitude);
            this.yourPin = new Microsoft.Maps.Pushpin(location, {
              title: "You",
              text: "5",
            });
            this.map.entities.push(this.yourPin);
            this.map.setView({ center: location, zoom: 16 });
            options.userLocation = location;
          }, null, { enableHighAccuracy: true });
        }

        // Get the exact location from bing maps
        const manager = new Microsoft.Maps.AutosuggestManager(options);
        manager.attachAutosuggest(
          this.searchBox,
          this.searchBoxContainer,
          (result) => {
            this.map.entities.remove(this.yourPin);
            this.map.entities.remove(this.binPin);
            this.yourPin = new Microsoft.Maps.Pushpin(result.location, {
              title: "You",
              text: "5",
            });
            this.map.entities.push(this.yourPin);
            this.map.setView({ center: result.location, zoom: 17 });
          }
        );
      });
  }

  onClassification(event: Classification) {
    this.category = event.category;
    // this.confidence = event.confidence.toString();
    const location = this.yourPin.getLocation();
    this.callApi(location.longitude, location.latitude);
  }

  callApi(longitude: number, latitude: number) {
    this.wasteTypeControllerService.calculateNearestCollectionPoint(this.category, `${latitude},${longitude}`).subscribe((result: any) => {
      var reader = new FileReader();
      reader.onload = () => {
        this.closestAddress = reader.result as string;
        const address = this.closestAddress.substring(this.closestAddress.indexOf('Adresse: ')+9);
        whenLoaded
        .then(() => loadModule(moduleNames.Search))
        .then(() => {
          this.map.entities.remove(this.binPin);
          const manager = new Microsoft.Maps.Search.SearchManager(this.map);
          const self = this;
          const options: Microsoft.Maps.Search.IGeocodeRequestOptions = {
            callback: function(geocodeResult: Microsoft.Maps.Search.IGeocodeResult, userData: any) {
              const result = geocodeResult.results.at(0);
              const location = result?.location;
              if (location) {
                self.binPin = new Microsoft.Maps.Pushpin(location, {
                  title: "Bin",
                  subTitle: result?.address.addressLine,
                  text: "5",
                  color: "green"
                });                
                self.map.entities.push(self.binPin);
                self.map.setView({ center: location, zoom: 17 });
              }
            },
            where: address,
            includeCountryIso2:true,            
          }
          manager.geocode(options);
        });
      }
      reader.readAsText(<Blob>result);
    });
  }
}