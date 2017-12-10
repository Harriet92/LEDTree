import { Component, OnInit, Input} from '@angular/core';
import { Mode } from '../mode';

@Component({
  selector: 'app-mode-detail',
  templateUrl: './mode-detail.component.html',
  styleUrls: ['./mode-detail.component.css']
})
export class ModeDetailComponent implements OnInit {

  @Input() mode: Mode;

  constructor() { }

  ngOnInit() {
  }

}
