import { HttpClient, HttpErrorResponse } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { environment } from '../../../environments/environment';

// Dialog
import { NbDialogService } from '@nebular/theme';

// RxJS
import { takeWhile } from 'rxjs/operators' ;
import { Observable } from 'rxjs/Observable';
import { mergeMap } from 'rxjs/operators';
import { throwError } from 'rxjs';
import { catchError, map } from 'rxjs/operators';

import { NbGlobalLogicalPosition, NbGlobalPhysicalPosition, NbGlobalPosition, NbComponentStatus } from '@nebular/theme';

@Injectable({
    providedIn: 'root'
})
export class FecalfaceImageService {  
      
    private data = {};  
    private globalResult: any = {};  
        
    private email: string;
    private username: string;
    public  response: any;
    private visualTasks: any;
    
    constructor(private http: HttpClient,
                private dialogService: NbDialogService) {}
    
    /* Global Data */
    public initialize() {  
        this.globalResult = {};
        console.log('dataService Initialize globalResult :', this.globalResult)
        return this.globalResult;
    }  
    
    public pushResult(key, value) {  
        this.globalResult[key] = value;
        console.log('dataService Push globalResult :', this.globalResult)
    }  
    
    public pullResult() {  
        console.log('dataService Pull globalResult :', this.globalResult)
        return this.globalResult;
    }  
    
    public removeResult(key) {  
        delete this.globalResult[key];
        console.log('dataService Remove globalResult :', this.globalResult)
    }  
    
    /* Http Service */
    // TODO : Use environment to set processUrl
    // private readonly processUrl: string = 'http://127.0.0.1:5000/';
    private readonly processUrl: string = environment.apiURL;
    
    // Get test
    public postTest$(): Observable<any> {
        return this.http.post<any>(this.processUrl + 'testing', 1);
    }
    
    // Generic GET request
    public getRequest$(url: string): Observable<any> {
        return this.http.get<any>(this.processUrl + url);
    }

    // Generic POST request
    public postRequest$(module: string, param: any): Observable<any> {
        console.log("POST ", this.processUrl + module, param);
        return this.http.post<any>(this.processUrl + module, param);
    }
    
    /* Get Avatar from instagram */
    public getInstagramAvatar(username: string, lang: string) {
      console.log('Get Instagram Avatar', this.processUrl);
      this.postRequest$('instagram', {username: username, lang: lang})
          .subscribe(this.responseAvatar,
                     err => console.error('Ops: ', err.message),
                     () => console.log('Completed Source')
      );
    }
    
    public detectFaceAvatar(image: string, lang: string) {
      console.log('Detect Face in Avatar');
      this.postRequest$('fecaldetect', {image_name: image, lang: lang})
          .subscribe(this.responseAvatar,
                     err => console.error('Ops: ', err.message),
                     () => console.log('Completed Detect')
      );
    }
     
    public makeupFaceAvatar(image: string) {
      console.log('Makeup Face in Avatar');
      this.postRequest$('fecalmakeup', {image_name: image})
          .subscribe(this.responseAvatar,
                     err => console.error('Ops: ', err.message),
                     () => console.log('Completed Makeup')
      );
    }
     
    public recogFaceAvatar(image: string) {
      console.log('Recognition Face in Avatar');
      this.postRequest$('fecalrecog', {image_name: image})
          .subscribe(this.responseAvatar,
                     err => console.error('Ops: ', err.message),
                     () => console.log('Completed Recognition')
      );
    }
     
    // Callbacks
    private responseAvatar = (data: any): any => {
        // this.globalResult['source'] = data;
        this.globalResult[data['module']] = data;
        console.log('************************************************************************');
        console.log('JSON :', this.globalResult);

        if (data['module'] == 'source' && data['status'] == 'Profile Ok') {
            console.log('Image', data['username'] + '.jpg');
            console.log('Launch face detect');
            this.detectFaceAvatar(data['username'] + '.jpg', this.globalResult['lang'])
        }
        if (data['module'] == 'detect' && data['status'] == "Face detected") {
            console.log('Launch face makeup');
            console.log('Image', this.globalResult['source']['username']);
            this.makeupFaceAvatar(this.globalResult['source']['username'] + '.jpg');
        }
        if (data['module'] == 'makeup') {
            console.log('Launch face recognition');
            console.log('Image', this.globalResult['source']['username']);
            this.recogFaceAvatar(this.globalResult['source']['username'] + '.jpg');
        }
        console.log('************************************************************************');
    }

    // Generic Callback
    private processResponse = (data: any): any => {
        this.response = data;
        let module_name = this.response.result[0].module;
        let param = this.response.result[1].param;
        console.log('************************************************************************');
        console.log('Module :', module_name);
        console.log('Param  :', param);
        console.log('************************************************************************');
    

        this.globalResult['taskresume'][0].PS++;
        this.globalResult[module_name] = data;

        for (let indexTaskexec in this.globalResult['taskexec']) {
            if (this.globalResult['taskexec'][indexTaskexec].module == module_name && 
                this.globalResult['taskexec'][indexTaskexec].param == param) {

                this.globalResult['taskexec'][indexTaskexec].state = "SUCCESS";
                console.log("State change..................SUCCESS");
                console.log(this.globalResult[module_name].result[2].validation);

                // Reprocess validation
                if (this.globalResult['taskexec'][indexTaskexec].score > 99) {
                    this.globalResult[module_name].result[2].validation = "hard";
                } else if (this.globalResult['taskexec'][indexTaskexec].score > 9) {
                    this.globalResult[module_name].result[2].validation = "soft";
                } else {
                    this.globalResult[module_name].result[2].validation = "no";
                }

            } 
        }

        console.log('Gathered :', this.globalResult);
    };
    
}  
