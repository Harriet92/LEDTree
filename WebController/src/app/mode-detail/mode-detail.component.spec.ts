import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { ModeDetailComponent } from './mode-detail.component';

describe('ModeDetailComponent', () => {
  let component: ModeDetailComponent;
  let fixture: ComponentFixture<ModeDetailComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ ModeDetailComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(ModeDetailComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
