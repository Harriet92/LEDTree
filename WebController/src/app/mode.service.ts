import { Injectable } from '@angular/core';
import { Mode } from './mode';
import { MODES } from './mock-modes';
import { Observable } from 'rxjs/Observable';
import { of } from 'rxjs/observable/of';
import { MessageService } from './message.service';
import { HttpClient, HttpHeaders } from '@angular/common/http';


@Injectable()
export class ModeService {

  private getModesUrl = 'http://192.168.0.3:8000/getmodes';
  private changeModeUrl = 'http://192.168.0.3:8000/change';


  constructor(
    private http: HttpClient,
    private messageService: MessageService) { }

  getModes(): Observable<Mode[]> {
    //this.messageService.add('ModeService: fetched modes');
    return this.http.get<Mode[]>(this.getModesUrl);
  }

  changeMode(mode: Mode): Observable<Mode> {
    const httpOptions = { headers: new HttpHeaders({ 'Content-Type': 'application/json' }) };
    this.messageService.add('Mode changed to: ' + mode.name);
    var obj = {
      mode: mode.name,
      args: {
        speed: mode.speed
        }
      };    
    return this.http.post<Mode>(this.changeModeUrl, JSON.stringify(obj), httpOptions);    
  }

  private log(message: string) {
    this.messageService.add('ModeService: ' + message);
  }

}
