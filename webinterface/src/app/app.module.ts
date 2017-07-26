import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { HttpModule } from '@angular/http';
import { AppRoutingModule } from './app-routing.module';
import { ReactiveFormsModule } from '@angular/forms';
import { TooltipModule } from "ngx-tooltip";

import { AppComponent } from './app.component';
import { ScenarioOneComponent } from './scenario-one/scenario-one.component';
import { ScenarioTwoComponent } from './scenario-two/scenario-two.component';
import { JobComponent } from './job/job.component';
import { SkillsComponent } from './skills/skills.component';
import { MethodComponent } from './method/method.component';

import { ApiService } from './services/api.service';
import { CvDetailComponent } from './cv-detail/cv-detail.component';
import { TEComponent } from './te/te.component';

@NgModule({
  declarations: [
    AppComponent,
    ScenarioOneComponent,
    ScenarioTwoComponent,
    JobComponent,
    SkillsComponent,
    MethodComponent,
    CvDetailComponent,
    TEComponent
  ],
  imports: [
    BrowserModule,
    FormsModule,
    HttpModule,
    AppRoutingModule,
    ReactiveFormsModule,
    TooltipModule
  ],
  providers: [ApiService],
  bootstrap: [AppComponent]
})
export class AppModule { }
