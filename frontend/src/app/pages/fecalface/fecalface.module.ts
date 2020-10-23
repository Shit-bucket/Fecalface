import { NgModule } from '@angular/core';
import {
  NbActionsModule,
  NbButtonModule,
  NbCardModule,
  NbCheckboxModule,
  NbDatepickerModule, NbIconModule,
  NbInputModule,
  NbRadioModule,
  NbSelectModule,
  NbUserModule,
  NbTooltipModule,
  NbStepperModule,
} from '@nebular/theme';

import { ThemeModule } from '../../@theme/theme.module';
import { FormsModule } from '@angular/forms';
import { AvatarComponent } from './avatar/avatar.component';
import { FecalfaceComponent } from './fecalface.component';

@NgModule({
  imports: [
    ThemeModule,
    FormsModule,
    NbInputModule,
    NbCardModule,
    NbUserModule,
    NbButtonModule,
    NbActionsModule,
    NbRadioModule,
    NbSelectModule,
    NbIconModule,
    NbButtonModule,
    NbTooltipModule,
    NbStepperModule,
  ],
  declarations: [
    FecalfaceComponent,
    AvatarComponent,
  ],
})
export class FecalfaceModule { }
