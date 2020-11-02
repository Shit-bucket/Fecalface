import { Component } from '@angular/core';

@Component({
  selector: 'ngx-pages',
  styleUrls: ['pages.component.scss'],
  template: `
    <ngx-layout-fecalface>
      <router-outlet></router-outlet>
    </ngx-layout-fecalface>
  `,
})
export class PagesComponent {

}
