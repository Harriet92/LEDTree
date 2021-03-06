import { Component, OnInit } from '@angular/core';
import { Mode } from '../mode';
import { ModeService } from '../mode.service';

@Component({
  selector: 'app-modes',
  templateUrl: './modes.component.html',
  styleUrls: ['./modes.component.css']
})
export class ModesComponent implements OnInit {
  
  modes: Mode[];
  selectedMode: Mode;

  constructor(private modeService: ModeService) { }
  
  onSelect(mode: Mode): void {
    this.selectedMode = mode;
  }

  getModes(): void {
    this.modeService.getModes()
      .subscribe(modes => this.modes = modes);
  }



  ngOnInit() {
    this.getModes();
  }

}
