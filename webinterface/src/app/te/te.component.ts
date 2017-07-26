import { Component, OnInit } from '@angular/core';
import { MyBarchart } from '../classes/myBarchart'
import { ApiService } from '../services/api.service';

@Component({
  selector: 'app-te',
  templateUrl: './te.component.html',
  styleUrls: ['./te.component.css']
})
export class TEComponent {

  charts: Array<MyBarchart> = []
  ctxArr = ['fp-entities-with-blacklist', 'fp-entities-newjobs-with-blacklist', 'fpreduced', 'fpreduced-newjobs']
  pagenums: Array<number>
  pageBtnDisabled: Array<boolean>
  PAGESIZE = 40
  titles = ['Tagme annotation with FP growth algorithm for jobs from 2016 summer',
    'Tagme annotation with FP growth algorithm for jobs from December 2016',
    'FP growth algorithm on jobs from 2016 summer', 'FP growth algorithm on jobs from December 2016']
  constructor(private apiService: ApiService) {
    this.pagenums = Array(this.ctxArr.length).fill(1);
    this.pageBtnDisabled = Array(this.ctxArr.length).fill(false)
  }

  ngAfterViewInit() {

    this.ctxArr.forEach((ctx, index) => {
      this.apiService.getBarchartData(ctx, this.pagenums[index])
        .then((response: Array<any>) => {
          this.drawGraph(response, index)
        })
    })
  }

  drawGraph(response: any, index: number){
     var labels = []
          var values = []
          Object.keys(response).forEach(key => {
            labels.push(response[key].labels.join(","))
            values.push(response[key].freq)
          })
          if (this.charts[index]) {
            this.charts[index].redrawGraph(this.ctxArr[index], labels, values, this.titles[index])
          } else {
            this.charts[index] = new MyBarchart(this.ctxArr[index], labels, values, this.titles[index])
          }
  }

  onPrevClicked(index): void {
    if ( this.pagenums[index] == 1 ) {return; }
    this.pagenums[index] = this.pagenums[index] - 1
    this.pageBtnDisabled[index] = false
     this.apiService.getBarchartData(this.ctxArr[index], this.pagenums[index])
    .then(response => {
      if (response.length < this.PAGESIZE){
        this.pageBtnDisabled[index] = true
      }
      this.drawGraph(response, index)
    })
  }

  onNextClicked(index): void {
    this.pagenums[index] = this.pagenums[index] + 1
    this.apiService.getBarchartData(this.ctxArr[index], this.pagenums[index])
    .then(response => {
      if (response.length < this.PAGESIZE){
        this.pageBtnDisabled[index] = true
      }
      this.drawGraph(response, index)
    })
  }

}
