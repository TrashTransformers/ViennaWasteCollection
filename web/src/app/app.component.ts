import { Component, Input } from '@angular/core';
import { WasteTypeControllerService } from './core/api/locate'
import { Classification } from './file-upload.component';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss']
})
export class AppComponent {

  title = 'WebApp';

  category: string = "";
  confidence: string = "";

  // Inject the generated Angular service as a dependency of this class
  constructor(private wasteTypeControllerService: WasteTypeControllerService) { }

  locate() {
    this.wasteTypeControllerService.calculateNearestCollectionPoint("plastic", "10.5,17.3").subscribe(x => {
      console.log(x);
    });
  }

  onClassification(event:Classification){
    this.category = event.category;
    this.confidence = event.confidence.toString();
  }
}