import { Component, Output, EventEmitter } from '@angular/core';

@Component({
    styleUrls: ['./method.component.css'],
    templateUrl: './method.component.html',
    selector: 'method'
})

export class MethodComponent {
    methods : string[] = ['tfidf', 'sgrank', 'jacc', 'lda', 'doc2vec', 'tfidf2'];
    unchecked: string = 'fa fa-circle-o fa-x';
    checked: string = 'fa fa-check-circle-o fa-x'
    checkedClass: string;
    radioClasses: Array<string>;
    @Output() onMethodChange = new EventEmitter<string>();
    tooltipTexts = ['TFIDF measure among jobs, cvs, and categories all together.',
     'sgrank model with cosine similarity among document key terms SGRank scores',
     'jacc model with Jaccard similarity among document key terms',
     'lda model with LDA topics similarity among documents',
     'doc2vec model with cosine similarity among document vectors from Doc2Vec',
     'tfidf2 pure TFIDF model using Gensim implementation'];
    constructor(){
        this.resetRadioClasses();
    }
    onClick(method: string, i: number){
        if(this.radioClasses[i] === this.checked){
            this.resetRadioClasses();
            this.onMethodChange.emit("");
        } else {
            this.resetRadioClasses();
            this.radioClasses[i] = this.checked;
            this.onMethodChange.emit(this.methods[i]);
        }
    }
    resetRadioClasses(){
        this.radioClasses = Array(this.methods.length).fill(this.unchecked);
    }
}
