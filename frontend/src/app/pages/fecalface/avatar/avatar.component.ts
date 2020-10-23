import { Component, OnInit, Input } from '@angular/core';

@Component({
  selector: 'ngx-avatar',
  templateUrl: 'avatar.component.html',
  styleUrls: ['avatar.component.scss'],
})
export class AvatarComponent {
  @Input() private data: any;
  public avatarDesc : string = "";
  public avatarName : string = "";
  public avatarSummary : string = "";
  public avatarURL : string = "";

  ngOnInit() {
    console.log("Avatar Component");

    if (this.data['module'] == 'source') {
      this.avatarName = this.data['d1'];
      this.avatarDesc = this.data['d2'];
      this.avatarSummary = this.data['d3'];
      if (this.data['url_img'] == undefined) {
        this.avatarURL = 'static/default/notfound.png';
      } else {
        this.avatarURL = this.data['url_img'];
      }
      console.log("Avatar URL", this.avatarURL);
    }

    if (this.data['module'] == 'detect') {
      this.avatarName = this.data['d1'];
      this.avatarDesc = this.data['d2'];
      this.avatarSummary = this.data['d3'];
      if (this.data['url_img'] == undefined) {
        this.avatarURL = 'static/default/undetected.png';
      } else {
        this.avatarURL = this.data['url_img'];
      }
      console.log("Avatar URL", this.avatarURL);
    }

    if (this.data['module'] == 'makeup') {
      this.avatarName = this.data['d1'];
      this.avatarDesc = this.data['d2'];
      this.avatarSummary = this.data['d3'];
      this.avatarURL = this.data['url_img'];
      console.log("Avatar URL", this.avatarURL);
    }

    if (this.data['module'] == 'recog') {
      this.avatarName = this.data['d1'];
      this.avatarDesc = this.data['d2'];
      this.avatarSummary = this.data['d3'];
      if (this.data['url_img'] == undefined) {
        this.avatarURL = 'static/default/notrecon.png';
      } else {
        this.avatarURL = this.data['url_img'];
      }
      console.log("Avatar URL", this.avatarURL);
    }
  }
}
