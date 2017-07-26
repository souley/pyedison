import { NgModule }             from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { ScenarioOneComponent } from './scenario-one/scenario-one.component'
import { ScenarioTwoComponent } from './scenario-two/scenario-two.component'
import { TEComponent } from './te/te.component';

const routes: Routes = [
  { path: '', redirectTo: '/scenario-two', pathMatch: 'full' },
  { path: 'scenario-one',  component: ScenarioOneComponent },
  { path: 'scenario-two', component: ScenarioTwoComponent},
  { path: 'te', component: TEComponent }
];

@NgModule({
  imports: [ RouterModule.forRoot(routes) ],
  exports: [ RouterModule ]
})

export class AppRoutingModule {}
