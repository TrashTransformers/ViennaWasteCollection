import "bingmaps";
import { initialize, loadModule, whenLoaded, moduleNames } from "bing-maps-loader";
import { WasteCollectionPointResponse, WasteTypeControllerService } from './core/api/locate'
import { Classification, FileUploadComponent } from './file-upload.component';
import { environment } from "src/environments/environment";
import { Component, OnInit, ViewChild } from "@angular/core";

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss']
})
export class AppComponent implements OnInit {
  
  @ViewChild('fileUpload') fileUpload: any;

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
            this.clear();
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

  onReloadCurrentPage() {
    window.location.reload();
  }

  onClassification(event: Classification) {
    const location = this.yourPin.getLocation();
    this.callApi(event.category, location.longitude, location.latitude);
  }

  callApi(category :string, longitude: number, latitude: number) {
    this.wasteTypeControllerService.calculateNearestCollectionPoint(category, `${latitude},${longitude}`).subscribe((result:any) => {
      var reader = new FileReader();
      reader.onload = () => {
        const response = JSON.parse(reader.result as string) as WasteCollectionPointResponse;
        const typeOfDisposal = response.typeOfDisposal as string
        this.closestAddress = response.address as string;
        whenLoaded
        .then(() => {
          this.map.entities.remove(this.binPin);
          const location = new Microsoft.Maps.Location(response.longitude, response.latitude);
          this.binPin = new Microsoft.Maps.Pushpin(location, {
            title: typeOfDisposal,
            subTitle: this.closestAddress,
            text: "5",
            color: "green"
          });
          this.map.entities.push(this.binPin);
          this.map.setView({ center: location, zoom: 17 });
        });
      }
      reader.readAsText(<Blob>result);
    });
  }

  clear() {
    this.closestAddress = "";    
    this.map.entities.remove(this.yourPin);
    this.map.entities.remove(this.binPin);
    (<FileUploadComponent>this.fileUpload).clear();
  }
}