import { Component } from '@angular/core';
import { DefaultService as ClassifyService } from './core/api/classify'
import { WasteTypeControllerService } from './core/api/locate'

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss']
})
export class AppComponent {

  title = 'WebApp';

  // Inject the generated Angular service as a dependency of this class
  constructor(private classifyService: ClassifyService,
    private wasteTypeControllerService: WasteTypeControllerService) {}

  classify() {
    this.classifyService.createFileClassifyPost(new Blob()).subscribe(x => {
      console.log(x);
    });
  }

  locate() {
    this.wasteTypeControllerService.calculateNearestCollectionPoint("plastic","10.5,17.3").subscribe(x => {
      console.log(x);
    });
  }
}