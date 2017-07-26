import { Component, Output, EventEmitter } from '@angular/core';
import { ApiService } from '../services/api.service';

@Component({
    selector: 'job',
    styleUrls: ['./job.component.css'],
    templateUrl: './job.component.html'
})

export class JobComponent {
    constructor(private apiService: ApiService){}
    jobPanelHeading = 'Job description'
    jobDescription: string;
    @Output() onJobChange = new EventEmitter<number>();
    getJob(jobid: string): void {
        this.apiService.getJob(jobid)
        .then(job => {
            if(job.description !== undefined){
                this.jobDescription = job.description;
                this.onJobChange.emit(job.jobid);
            } else {
                this.jobDescription = `No job with id ${jobid} found.`;
            }
            this.jobDescription = job.description !== undefined ? job.description : `No job with id ${jobid} found.`;
        })
    }


}
