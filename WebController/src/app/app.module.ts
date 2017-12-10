import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { ModesComponent } from './modes/modes.component';
import { AppComponent } from './app.component';
import { ModeDetailComponent } from './mode-detail/mode-detail.component';
import { ModeService } from './mode.service';
import { MessageService } from './message.service';
import { MessagesComponent } from './messages/messages.component';
import { HttpClientModule } from '@angular/common/http';

@NgModule({
  declarations: [
    AppComponent,
    ModesComponent,
    ModeDetailComponent,
    MessagesComponent
  ],
  imports: [
    BrowserModule,
    FormsModule,
    HttpClientModule
  ],
  providers: [ ModeService, MessageService ],
  bootstrap: [AppComponent]
})
export class AppModule { }
