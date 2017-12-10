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
  
  onSelect(mode: Mode): void {
    this.selectedMode = mode;
    this.changeMode(mode);
  }

  getModes(): void {
    this.modeService.getModes()
      .subscribe(modes => this.modes = modes);
  }

  changeMode(mode: Mode): void {
    this.modeService.changeMode(mode)
      .subscribe(e => console.log(e));
  }

  constructor(private modeService: ModeService) { }

  ngOnInit() {
    this.getModes();
  }

}
