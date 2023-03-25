import { NgModule, isDevMode } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { ServiceWorkerModule } from '@angular/service-worker';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';

import { HttpClientModule } from '@angular/common/http';
import { environment } from '../environments/environment';
import { ApiModule as ClassifyModule } from './core/api/classify/api.module';
import { Configuration as ClassifyConfiguration, ConfigurationParameters as ClassifyConfigurationParameters} from './core/api/classify';
import { ApiModule as LocateModule } from './core/api/locate/api.module';
import { Configuration as LocateConfiguration, ConfigurationParameters as LocateConfigurationParameters} from './core/api/locate';


export function classifyApiConfigFactory(): ClassifyConfiguration {
  const params: ClassifyConfigurationParameters = {
    basePath: environment.basePath,
  };
  return new ClassifyConfiguration(params);
}

export function locateApiConfigFactory(): LocateConfiguration {
  const params: LocateConfigurationParameters = {
    basePath: environment.basePath,
  };
  return new LocateConfiguration(params);
}

@NgModule({
  declarations: [
    AppComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    ServiceWorkerModule.register('ngsw-worker.js', {
      enabled: !isDevMode(),
      // Register the ServiceWorker as soon as the application is stable
      // or after 30 seconds (whichever comes first).
      registrationStrategy: 'registerWhenStable:30000'
    }),
    BrowserAnimationsModule,

    // make sure to import the HttpClientModule in the AppModule only,
    // see https://github.com/angular/angular/issues/20575
    HttpClientModule,
    ClassifyModule.forRoot(classifyApiConfigFactory),
    LocateModule.forRoot(locateApiConfigFactory),
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
