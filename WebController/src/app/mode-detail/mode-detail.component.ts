import { Component, OnInit, Input, HostListener} from '@angular/core';
import { Mode } from '../mode';
import { Arg } from '../mode';
import { HttpClient, HttpHeaders } from '@angular/common/http';

import { ModeService } from '../mode.service';

@Component({
  selector: 'app-mode-detail',
  templateUrl: './mode-detail.component.html',
  styleUrls: ['./mode-detail.component.css']
})
export class ModeDetailComponent implements OnInit {

  private changeModeUrl = 'http://192.168.0.3:8000/change';
  @Input() mode: Mode;

  constructor(private http: HttpClient, private modeService: ModeService) { }

  ngOnInit() {
  }

  changeColor(value): void {
    console.log(value);
    this.modeService.changeMode(this.mode)
      .subscribe(e => console.log(e));
  }

  changeSpeed(value): void {
    console.log(value);
    this.modeService.changeMode(this.mode)
      .subscribe(e => console.log(e));
  }

  onSelect(event: any): void {
    const httpOptions = { headers: new HttpHeaders({ 'Content-Type': 'application/json' }) };  
    this.http.post(this.changeModeUrl, JSON.stringify(event.target.value), httpOptions); 
  }
}
