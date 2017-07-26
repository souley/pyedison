import { Injectable }    from '@angular/core';
import { Headers, Http } from '@angular/http';
import 'rxjs/add/operator/toPromise';
import { Job } from '../classes/job';
import { Skill } from '../classes/skill';
import { Observable }     from 'rxjs/Observable';
import 'rxjs/add/operator/map';

@Injectable()
export class ApiService {
    private baseUrl = 'http://localhost:5000';
    private headers = new Headers({ 'Content-Type': 'application/json' });
    constructor(private http: Http) { }

    private handleError(error: any): Promise<any> {
        console.error('An error occurred', error); // for demo purposes only
        return Promise.reject(error.message || error);
    }

     getJob(id: string): Promise<Job> {
         const url = `${this.baseUrl}/job/${id}`;
             return this.http.get(url)
                 .toPromise()
                 .then(response => response.json().response as Job)
                 .catch(this.handleError);
        }

     getSkill(term: string): Promise<Skill> {
         const url = `${this.baseUrl}/skill/${term}`;
         return this.http
             .get(url)
             .toPromise()
             .then(response => response.json().response as Skill)
             .catch(this.handleError);
         }

     searchSkill(term: string): Observable<Skill[]> {
         const url = `${this.baseUrl}/skillrec?q=${term}`
         return this.http
            .get(url)
            .map(response => {
                return response.json().response as Skill[]
            });
     }

     getGraphData(jobid: number, method: string, skills: Array<Skill>, pagenum: number): Promise<any>{
         const url = `${this.baseUrl}/graph`;
         return this.http
            .post(url, {jobid: jobid, method: method, cat_id_1: skills[0].catid,
            cat_id_2: skills[1].catid, cat_id_3: skills[2].catid,
            cat_id_4: skills[3].catid, cat_id_5: skills[4].catid, pagenum: pagenum})
            .toPromise()
            .then(response => {
                return response.json().response;
            })
            .catch(this.handleError);
     }

     getEdisonGraphData(jobid: number, method: string, pagenum: number): Promise<any> {
         const url = `${this.baseUrl}/edisongraph`;
         return this.http
            .post(url, {jobid: jobid, method: method, pagenum: pagenum})
            .toPromise()
            .then(response => {
                return response.json().response;
            })
            .catch(this.handleError);
     }

     getEdisonSkills(): Promise<any> {
         const url = `${this.baseUrl}/edisonskills`;
         return this.http
            .get(url)
            .toPromise()
            .then(response => {
                return response.json().response;
            })
            .catch(this.handleError)
     }

     getEdisonGraphCV(cvid: string, jobid:number, method: string): Promise<any> {
         const url = `${this.baseUrl}/edisongraphcv`;
         return this.http
            .post(url, {jobid: jobid, cvid: cvid, method: method})
            .toPromise()
            .then(response => {
                return response.json().response;
            })
            .catch(this.handleError);
     }

     getSingleEdsionGraphCV(cvid: string, jobid:number, method: string, skills: Array<Skill>): Promise<any>{
         const url = `${this.baseUrl}/singleedisongraphcv`;
         return this.http
            .post(url, {jobid: jobid, cvid: cvid, method: method, cat_id_1: skills[0].catid,
                        cat_id_2: skills[1].catid, cat_id_3: skills[2].catid,
                        cat_id_4: skills[3].catid, cat_id_5: skills[4].catid})
            .toPromise()
            .then(response => {
                return response.json().response;
            })
            .catch(this.handleError);
     }

     getCV(cvid: string){
         const url = `${this.baseUrl}/cv/${cvid}`;
         return this.http
            .get(url)
            .toPromise()
            .then(response => {
                return response.json().response;
            })
            .catch(this.handleError);
     }

     getBarchartData(type: string, pagenum: number): Promise<any>{
         const url = `${this.baseUrl}/barchart`;
          return this.http
            .post(url, {chart_type: type, pagenum: pagenum})
            .toPromise()
            .then(response => {
                return response.json().response;
            })
            .catch(this.handleError);
     }

     getEdisonGraphData4Cat(catid: number, method: string, pagenum: number): Promise<any> {
         const url = `${this.baseUrl}/edisongraph4cat`;
         return this.http
            .post(url, {catid: catid, method: method, pagenum: pagenum})
            .toPromise()
            .then(response => {
                return response.json().response;
            })
            .catch(this.handleError);
     }
}
