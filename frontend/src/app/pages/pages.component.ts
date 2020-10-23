import { Component } from '@angular/core';

import { MENU_ITEMS } from './pages-menu';

@Component({
  selector: 'ngx-pages',
  styleUrls: ['pages.component.scss'],
  template: `
    <ngx-layout-fecalface>
      <!-- <nb-menu [items]="menu"></nb-menu> -->
      <router-outlet></router-outlet>
    </ngx-layout-fecalface>
  `,
})
export class PagesComponent {

  menu = MENU_ITEMS;
}
