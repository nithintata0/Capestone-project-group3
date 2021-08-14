import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { NZ_I18N } from 'ng-zorro-antd/i18n';
import { en_US } from 'ng-zorro-antd/i18n';
import { registerLocaleData } from '@angular/common';
import en from '@angular/common/locales/en';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { HttpClientModule } from '@angular/common/http';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { HomeComponent } from './home/home.component';
import { AngularFireModule } from '@angular/fire';
import { environment } from '../environments/environment';
import { ShowJobsComponent } from './show-jobs/show-jobs.component';
import { NzCardModule } from 'ng-zorro-antd/card';
import { AddJobComponent } from './add-job/add-job.component';
import { NzFormModule } from 'ng-zorro-antd/form';
import { NzInputModule } from 'ng-zorro-antd/input';
import { NzButtonModule } from 'ng-zorro-antd/button';
registerLocaleData(en);
import { CKEditorModule } from '@ckeditor/ckeditor5-angular';
import {AngularFireStorageModule, BUCKET } from '@angular/fire/storage';
import { AdminComponent } from './admin/admin.component';
import { NzIconModule } from 'ng-zorro-antd/icon';
import * as AllIcons from '@ant-design/icons-angular/icons';
import { NZ_ICONS } from 'ng-zorro-antd/icon';
import { IconDefinition } from '@ant-design/icons-angular';
import { AdminViewProfileComponent } from './admin-view-profile/admin-view-profile.component';
import { AdminHeaderComponent } from './admin-header/admin-header.component';
import { NzDrawerModule } from 'ng-zorro-antd/drawer';

const antDesignIcons = AllIcons as {
  [key: string]: IconDefinition;
};
const icons: IconDefinition[] = Object.keys(antDesignIcons).map(key => antDesignIcons[key])
@NgModule({
  declarations: [
    AppComponent,
    HomeComponent,
    ShowJobsComponent,
    AddJobComponent,
    AdminComponent,
    AdminViewProfileComponent,
    AdminHeaderComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    FormsModule,
    HttpClientModule,
    BrowserAnimationsModule,
    NzDrawerModule,
    NzCardModule,
    NzFormModule,
    FormsModule,
    ReactiveFormsModule,
    NzInputModule,
    NzButtonModule,
    AngularFireStorageModule,
    NzIconModule,
    
    CKEditorModule,
    AngularFireModule.initializeApp(environment.firebase)
  ],
  providers: [{ provide: NZ_I18N, useValue: en_US },  { provide: BUCKET, useValue: 'capestone-945f7.appspot.com' }, { provide: NZ_ICONS, useValue: icons } ],
  
  bootstrap: [AppComponent]
})
export class AppModule { }
