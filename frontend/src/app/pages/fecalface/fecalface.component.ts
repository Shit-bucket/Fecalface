import { Component, OnDestroy, AfterViewInit, ViewChild, OnInit } from '@angular/core';
import { NbThemeService } from '@nebular/theme';
import { takeWhile } from 'rxjs/operators' ;
import { NbDialogService } from '@nebular/theme';
import { NbStepperComponent } from '@nebular/theme';

import { FecalfaceImageService } from '../../@core/data/fecalface-image.service';

@Component({
    selector: 'ngx-fecalface',
    styleUrls: ['./fecalface.component.scss'],
    templateUrl: './fecalface.component.html',
})
export class FecalfaceComponent implements OnInit, OnDestroy {
    @ViewChild('stepper', { static: false }) public stepper: NbStepperComponent;

    private alive = true;
    public flipped: Boolean = false;
    public selectedLang: string = "spanish";
    public selectedItem: string = "instagram";
    public selectedStep: string = "Detect";
    public result: any;

    constructor(private fecalfaceImageService: FecalfaceImageService) { }

    ngOnInit() {
        this.result = [];
    }

    toggleFlipViewAndProcess(lang, rrss, username) {
        console.log("lang", this.selectedLang);
        console.log("rrss", this.selectedItem);
        console.log("username", username);

        this.flipped = !this.flipped;
        
        this.result = this.fecalfaceImageService.initialize();
        console.log("Global data initialize", this.result);

        this.result = this.fecalfaceImageService.pushResult("lang", lang);
        this.result = this.fecalfaceImageService.getInstagramAvatar(username, this.selectedLang); 
        this.result = this.fecalfaceImageService.pullResult();

        console.log("Global result", this.result);
    }

    toggleFlipView() {
        this.flipped = !this.flipped;
    }
     
    ngOnDestroy() {
      this.alive = false;
    }

    toDataURL(url) {
      return fetch(url)
        .then(response => {
          return response.blob();
        })
        .then(blob => {
          return URL.createObjectURL(blob);
        });
    }

    async downloadImg(url: string) {
      console.log("Image : ", url)
      const a = document.createElement("a");
      a.href = await this.toDataURL("http://127.0.0.1:5000" + url);
      a.download = "avatar-fecalface.jpg";
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
    }
}
