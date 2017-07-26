import { Component, ViewChild } from '@angular/core';
import { ApiService } from '../services/api.service';
import { MyChart } from '../classes/myChart';
import { CvDetailComponent } from '../cv-detail/cv-detail.component';

@Component({
    selector: 'scenario-two',
    templateUrl: './scenario-two.component.html',
    styleUrls: [ './scenario-two.component.css' ]
})


export class ScenarioTwoComponent {
    title = 'Scenario Two'
    jobid: number;
    method: string;
    skills: Array<string> = [];
    notEnoughParametersStr = 'Not enough parameters to draw the graphs.';
    displayGraph = false;
    ctxArr: Array<string> = ["mychart", "mychart2", "mychart3", "mychart4", "mychart5", "mychart6"];
    charts: Array<MyChart> = [];
    pagenum = 1;
    PAGESIZE = 6;
    loadMoreHidden = false;
    cvTabActive = false;
    graphsAvailable = false;
    @ViewChild(CvDetailComponent) cvDetail: CvDetailComponent;
    page = "sc2"
    constructor(private apiService:ApiService){}

    onJobChange(jobid: number): void {
        this.jobid = jobid;
        this.attemptToDraw();
    }
    onMethodChange(method: string): void {
        this.method = method;
        this.attemptToDraw();
    }

    attemptToDraw(): void {
        this.pagenum = 1;
        this.loadMoreHidden = false;
        this.ctxArr = this.ctxArr.slice(0, this.PAGESIZE);
        this.cvDetail.reset();
        if(this.method && this.jobid){
            this.apiService.getEdisonGraphData(this.jobid, this.method, this.pagenum)
                .then(response => {
                    this.drawGraph(response);
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
        var labels = Object.keys(json.cv_differences[0].skill_differences);
        var jobDiffArr = [];
        labels.forEach(label => jobDiffArr.push(json.job_diff[label]))
        json.cv_differences.forEach((obj, index) => {
            var cvDiffArr = []
            labels.forEach(label => cvDiffArr.push(obj.skill_differences[label]))
            var calculatedIndex = index + ((this.pagenum-1)*this.PAGESIZE);
            if(this.charts.length < this.ctxArr.length) {
                this.charts[calculatedIndex] = new MyChart(this.ctxArr[calculatedIndex], labels, `CV ${obj.cvid}`, cvDiffArr, `Job ${this.jobid}`, jobDiffArr);
            } else {
                this.charts[calculatedIndex].redrawGraph(this.ctxArr[calculatedIndex], labels, `CV ${obj.cvid}`, cvDiffArr, `Job ${this.jobid}`, jobDiffArr);
            }
        })
    }

    loadMore(): void {
        this.pagenum += 1;
        for(var i = 0; i < this.PAGESIZE; i++){
            this.ctxArr.push(this.getGuid());
        }
        this.apiService.getEdisonGraphData(this.jobid, this.method, this.pagenum)
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
