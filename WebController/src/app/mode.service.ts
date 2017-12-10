import { Injectable } from '@angular/core';
import { Mode } from './mode';
import { MODES } from './mock-modes';
import { Observable } from 'rxjs/Observable';
import { of } from 'rxjs/observable/of';
import { MessageService } from './message.service';
import { HttpClient, HttpHeaders } from '@angular/common/http';

@Injectable()
export class ModeService {

  private modesUrl = 'http://192.168.0.3:8000/getmodes';

  constructor(
    private http: HttpClient,
    private messageService: MessageService) { }

  getModes(): Observable<Mode[]> {
    //this.messageService.add('ModeService: fetched modes');
    return this.http.get<Mode[]>(this.modesUrl);
  }

  private log(message: string) {
    this.messageService.add('ModeService: ' + message);
  }

}
