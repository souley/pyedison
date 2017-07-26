import { Component, Input } from '@angular/core';
import { ApiService } from '../services/api.service';
import { MyChart } from '../classes/myChart';
import { Skill } from '../classes/skill';

@Component({
  selector: 'cv-detail',
  templateUrl: './cv-detail.component.html',
  styleUrls: ['./cv-detail.component.css']
})
export class CvDetailComponent {

  @Input() jobid: number;
  @Input() method: string;
  @Input() page: string;
  @Input() skills?: Array<Skill>;
  graph: MyChart;
  graphstr = "cv-detail";
  cvDescription: string;
  hideCvDescription = true;
  hideGraph: boolean;
  inputValue: string;
  constructor(private apiService: ApiService){}

  reset(): void {
      this.hideCvDescription = true;
      this.hideGraph = true;
      this.inputValue = "";
  }

  getCV(cvid: string): void{
      if(this.page=='sc2'){
          this.apiService.getEdisonGraphCV(cvid, this.jobid, this.method)
          .then(json => {
              this.drawGraph(json);
              this.apiService.getCV(cvid).then(cv => this.cvDescription = cv.description)
              this.hideCvDescription = false;
              this.hideGraph = false;
          }).catch(e => console.log(e));
      }   else if(this.page == 'sc1'){
          this.apiService.getSingleEdsionGraphCV(cvid, this.jobid, this.method, this.skills)
            .then(json => {
                this.drawGraph(json);
                this.apiService.getCV(cvid).then(cv => this.cvDescription = cv.description)
                this.hideCvDescription = false;
                this.hideGraph = false;
            })
    }
  }

  drawGraph(json: any): void{
      var labels = Object.keys(json.skill_differences);
      var cvDiffArr = [];
      var jobDiffArr = [];
      labels.forEach(label => {
          cvDiffArr.push(json.skill_differences[label])
          jobDiffArr.push(json.job_diff[label])
      });
      if(!this.graph){
          this.graph = new MyChart(this.graphstr, labels, `CV ${json.cvid}`, cvDiffArr, `Job ${this.jobid}`, jobDiffArr)
      } else {
          this.graph.redrawGraph(this.graphstr, labels, `CV ${json.cvid}`, cvDiffArr, `Job ${this.jobid}`, jobDiffArr);
      }
  }

}
