import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { UpdatesListComponent } from './components/updates-list/updates-list.component';

const routes: Routes = [
  { path: '', redirectTo: 'updates', pathMatch: 'full' },
  { path: 'updates', component: UpdatesListComponent },
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
