import { Component, OnInit } from '@angular/core';
import { Mode } from '../mode';
import { MODES } from '../mock-modes';
import * as child_process from 'child_process';

@Component({
  selector: 'app-modes',
  templateUrl: './modes.component.html',
  styleUrls: ['./modes.component.css']
})
export class ModesComponent implements OnInit {
  
  py: any;
  modes = MODES;
  selectedMode: Mode;
  
  onSelect(mode: Mode): void {
    this.selectedMode = mode;
    this.sendSignal(mode);
  }

  sendSignal(mode: Mode): void {
    var data = '{"mode":"rainbowCycle"}';
    this.py.stdin.write(data);
    this.py.stdin.end();
  }

  constructor() { }

  ngOnInit() {
    var spawn = child_process.spawn;
    this.py = spawn('python', ['/home/pi/LEDTree/LedController/maincontroller.py']);
    var dataString = '';

    this.py.stdout.on('data', function(data){
      dataString += data.toString();
    });

    this.py.stdout.on('end', function(){
      console.log('RETURNED=',dataString);
    });
  }

}
