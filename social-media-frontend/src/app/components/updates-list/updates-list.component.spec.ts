import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { UpdatesListComponent } from './updates-list.component';

describe('UpdatesListComponent', () => {
  let component: UpdatesListComponent;
  let fixture: ComponentFixture<UpdatesListComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ UpdatesListComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(UpdatesListComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
