import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { ModesComponent } from './modes/modes.component';
import { AppComponent } from './app.component';
import { ModeDetailComponent } from './mode-detail/mode-detail.component';


@NgModule({
  declarations: [
    AppComponent,
    ModesComponent,
    ModeDetailComponent
  ],
  imports: [
    BrowserModule,
    FormsModule
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
