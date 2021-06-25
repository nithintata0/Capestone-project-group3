import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { HomeComponent } from './home/home.component';
import { ShowJobsComponent } from './show-jobs/show-jobs.component';
import { AddJobComponent } from './add-job/add-job.component';
import { AdminComponent } from './admin/admin.component';

const routes: Routes = [
  {
    path: '',
    redirectTo: 'home',
    pathMatch: 'full'
  },
  {
    path:"home",
    component:HomeComponent
  },
  {
    path:"jobs",
    component:ShowJobsComponent
  },
  {
    path:"add-jobs",
    component:AddJobComponent
  },
  {
    path:'admin',
    component:AdminComponent
  }
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
