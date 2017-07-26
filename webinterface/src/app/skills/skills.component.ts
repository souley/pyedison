import { Component, OnInit, Output, EventEmitter  } from '@angular/core';
import { Skill } from '../classes/skill'
import { Subject } from 'rxjs/Subject';
import { Observable } from 'rxjs/Observable';
import { ApiService } from '../services/api.service';

import 'rxjs/add/observable/of';
import 'rxjs/add/observable/empty';
import 'rxjs/add/operator/catch';
import 'rxjs/add/operator/debounceTime';
import 'rxjs/add/operator/distinctUntilChanged';
import 'rxjs/add/operator/switchMap';

@Component({
    selector: 'skills',
    styleUrls: ['skills.component.css'],
    templateUrl: 'skills.component.html'
})

export class SkillsComponent implements OnInit{
    private SKILL_NUM = 5;
    skills: Skill[] = new Array<Skill>();
    showTable: boolean = false;
    noSkillsText: string = 'No skills added yet.';
    recomendedSkills: Observable<Skill[]>;
    inputValue: string = '';
    inputDisabled: boolean = false;
    hideSearch: boolean = true;
    private searchTerms = new Subject<string>();
    @Output() onSkillChange = new EventEmitter<Array<Skill>>();

    constructor(private apiService: ApiService){}

    ngOnInit(){
        this.recomendedSkills = this.searchTerms
            .debounceTime(300)
            .distinctUntilChanged()
            .switchMap(term => {
            if (term.length >= 1) {
                 if(this.inputValue.length > 0){
                     this.hideSearch = false;
                 }
                 return this.apiService.searchSkill(term);
            } else {
                this.hideSearch = true;
                return Observable.of<Skill[]>([])
            }
    })
      .catch(error => {
        console.log(error);
        return Observable.of<Skill[]>([]);
      });
    }

    addSkill(skillName: string): void {
        if (skillName){
            this.apiService.getSkill(skillName)
            .then(skill => {
                if (skill.catid){
                    var duplicate = false;
                    this.skills.forEach(el => {
                        if (el.catid == skill.catid){
                            duplicate = true;
                        }
                    });
                if (!duplicate){
                    this.skills.push(skill as Skill);
                    this.showTable = true;
                    this.inputValue = "";
                    this.hideSearch = true;
                    this.inputDisabled = this.skills.length == this.SKILL_NUM;
                    this.onSkillChange.emit(this.skills);
                }
            }})
            .catch(error => {
                console.log(error);
            })
        }
    }

    recSelected(rec: Skill): void{
        this.inputValue = rec.skillName;
        this.hideSearch = true;
    }

    recSkills(term: string): void {
        this.searchTerms.next(term);
    }
    removeSkill(skill: Skill): void{
        this.skills.forEach((el, index) => {
            if (el.catid == skill.catid){
                this.skills.splice(index ,1)
                this.inputDisabled = false;
                this.onSkillChange.emit(this.skills);
                this.showTable = !(this.skills.length == 0);
            }
        })
    }
}
