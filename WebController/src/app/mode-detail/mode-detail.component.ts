import { Component, OnInit, Input, HostListener} from '@angular/core';
import { Mode } from '../mode';
import { Arg } from '../mode';
import { HttpClient, HttpHeaders } from '@angular/common/http';

@Component({
  selector: 'app-mode-detail',
  templateUrl: './mode-detail.component.html',
  styleUrls: ['./mode-detail.component.css']
})
export class ModeDetailComponent implements OnInit {

  private changeModeUrl = 'http://192.168.0.3:8000/change';
  @Input() mode: Mode;

  constructor(private http: HttpClient) { }

  ngOnInit() {
  }

  ngOnChanges() {
    console.log(`ngOnChanges - data is ${this.mode}`);
  }

 @HostListener('ngModelChange', ['$event'])
 onChange(event) {
   console.log(event);
}

  onSelect(event: any): void {
    const httpOptions = { headers: new HttpHeaders({ 'Content-Type': 'application/json' }) };  
    this.http.post(this.changeModeUrl, JSON.stringify(event.target.value), httpOptions); 
  }
}
