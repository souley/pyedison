import { Component, ViewChild } from '@angular/core'
import { MyChart } from '../classes/myChart';
import { Skill } from '../classes/skill';
import { ApiService } from '../services/api.service';
import { CvDetailComponent } from '../cv-detail/cv-detail.component';

@Component({
    selector: 'scenario-one',
    templateUrl: './scenario-one.component.html',
    styleUrls: ['./scenario-one.component.css']
})

export class ScenarioOneComponent {
    title = 'Scenario 1';
    notEnoughParametersStr = 'Not enough parameters to draw the graphs.';
    SKILL_NUM = 5;
    jobid: number;
    method: string;
    skills: Array<Skill>;
    displayGraph = false;
    ctxArr: Array<string> = ["mychart", "mychart2", "mychart3", "mychart4", "mychart5", "mychart6"];
    charts: Array<MyChart> = [];
    pagenum = 1;
    PAGESIZE = 6;
    loadMoreHidden = false;
    cvTabActive = false;
    graphsAvailable = false;
    @ViewChild(CvDetailComponent) cvDetail: CvDetailComponent;
    page = "sc1";
    constructor(private apiService: ApiService){}

  onJobChange(jobid: number): void {
      this.jobid = jobid;
      this.attemptToDraw();
  }

  onMethodChange(method: string): void {
      this.method = method;
      this.attemptToDraw();
  }

  onSkillChange(skills: Array<Skill>): void {
      this.skills = skills;
      this.attemptToDraw();
  }

  attemptToDraw(): void {
     this.pagenum = 1;
     this.loadMoreHidden = false;
     this.ctxArr = this.ctxArr.slice(0, this.PAGESIZE);
     this.cvDetail.reset();
     if (this.method && this.jobid && (this.skills && this.skills.length == this.SKILL_NUM) ) {
         this.apiService.getGraphData(this.jobid, this.method, this.skills, this.pagenum)
         .then(json => {
              this.drawGraph(json)
              this.displayGraph = true;
              this.graphsAvailable = true;
              this.cvTabActive = false;
         })
         .catch(error => {
             console.log(error);
             return;
         })

     } else {
         this.displayGraph = false;
         this.graphsAvailable = false;
         this.cvTabActive = false;
     }
  }

  drawGraph(json: any): void {
      var labels = [];
      this.skills.forEach(skill => labels.push(skill.skillName));
      var jobid = json.job_diff.jobid;
      var jobDiffArr = [json.job_diff.cat_1_diff,  json.job_diff.cat_2_diff, json.job_diff.cat_3_diff, json.job_diff.cat_4_diff, json.job_diff.cat_5_diff];
      json.cv_differences.forEach((obj, index) => {
          var cvDiffArr = [obj.cat_1_diff, obj.cat_2_diff, obj.cat_3_diff, obj.cat_4_diff, obj.cat_5_diff];
          var calculatedIndex = index + ((this.pagenum-1)*this.PAGESIZE);
          if(this.charts.length < this.ctxArr.length) {
              this.charts[calculatedIndex] = new MyChart(this.ctxArr[calculatedIndex], labels, `CV ${obj.cvid}`, cvDiffArr, `Job ${jobid}`, jobDiffArr);
          } else {
              this.charts[calculatedIndex].redrawGraph(this.ctxArr[calculatedIndex], labels, `CV ${obj.cvid}`, cvDiffArr, `Job ${jobid}`, jobDiffArr);
          }
      })
  }

  loadMore(): void {
      this.pagenum += 1;
      for(var i = 0; i < this.PAGESIZE; i++){
          this.ctxArr.push(this.getGuid());
      }
      this.apiService.getGraphData(this.jobid, this.method, this.skills, this.pagenum)
      .then(json => {
          if (json.cv_differences.length > 0){
              if(json.cv_differences.length < this.PAGESIZE){
                  this.loadMoreHidden = true;
              }
              this.drawGraph(json);
          } else {
              this.loadMoreHidden = true;
          }
      })
      .catch(error => {
          console.log(error);
          return;
      })
  }

  getGuid(): string {
      return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function(c) {
          var r = Math.random()*16|0, v = c === 'x' ? r : (r&0x3|0x8);
          return v.toString(16);
      });
    }

    onTabChange(index: number){
       if(index == 0 && this.cvTabActive){
           this.cvTabActive = false;
           this.displayGraph = true;
       }
       if(index == 1 && !this.cvTabActive){
           this.cvTabActive = true;
           this.displayGraph = false;
       }
    }
}
