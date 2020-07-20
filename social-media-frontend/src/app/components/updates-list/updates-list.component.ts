import { Component, OnInit } from '@angular/core';
import { UpdatesService } from 'src/app/services/updates.service';
import {Observable, Subscription, timer} from "rxjs";

@Component({
  selector: 'app-updates-list',
  templateUrl: './updates-list.component.html',
  styleUrls: ['./updates-list.component.css']
})
export class UpdatesListComponent implements OnInit {

  updates: any;
  title = '';
  subscription: Subscription;
  everyFiveSeconds: Observable<number> = timer(0, 5000);

  constructor(private updatesService: UpdatesService) { }

  ngOnInit(): void {
    this.subscription = this.everyFiveSeconds.subscribe(() => {
      this.retrieveUpdates();
    });
  }

  retrieveUpdates(): void {
    this.updatesService.getAll()
      .subscribe(
        data => {
          this.updates = data.data;
          console.log(data);
        },
        error => {
          console.log(error);
        });
  }
}
