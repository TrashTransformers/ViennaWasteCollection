import { Component, Input } from '@angular/core';
import { WasteTypeControllerService } from './core/api/locate'
import { Classification } from './file-upload.component';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss']
})
export class AppComponent {

  category: string = "";
  confidence: string = "";
  closestAddress: string = "";

  // Inject the generated Angular service as a dependency of this class
  constructor(private wasteTypeControllerService: WasteTypeControllerService) { }

  locate() {
    this.wasteTypeControllerService.calculateNearestCollectionPoint("plastic", "10.5,17.3").subscribe(x => {
      console.log(x);
    });
  }

  onClassification(event: Classification) {
    this.category = event.category;
    this.confidence = event.confidence.toString();
    this.getLocation();
  }

  getLocation(): void {
    if (navigator.geolocation) {
      navigator.geolocation.getCurrentPosition((position) => {
        const longitude = position.coords.longitude;
        const latitude = position.coords.latitude;
        this.callApi(longitude, latitude);
      }, null, {enableHighAccuracy: true});
    } else {
      console.log("No support for geolocation")
    }
  }

  callApi(longitude: number, latitude: number) {
    this.wasteTypeControllerService.calculateNearestCollectionPoint(this.category, `${latitude},${longitude}`).subscribe((result: any) => {
      var reader = new FileReader();
      reader.onload = () => {
        this.closestAddress = reader.result as string;
      }
      reader.readAsText(<Blob>result);
    });
  }
}