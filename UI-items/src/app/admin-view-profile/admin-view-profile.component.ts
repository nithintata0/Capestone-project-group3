import { Component, OnInit } from '@angular/core';
import { AngularFireAuth } from '@angular/fire/auth';
import { AngularFirestore } from '@angular/fire/firestore';
import { Router } from '@angular/router';
import * as _ from 'lodash';

@Component({
  selector: 'app-admin-view-profile',
  templateUrl: './admin-view-profile.component.html',
  styleUrls: ['./admin-view-profile.component.scss']
})
export class AdminViewProfileComponent implements OnInit {
  userName = ""
  jobsProfiles = []
  jobAppliedUsers = []

  userApplication: any
  unFliteredJobAppledUser = []

  constructor(private auth: AngularFireAuth, private router: Router, private afs: AngularFirestore,) {

  }

  ngOnInit(): void {
    this.afs.collection('jobs').get().subscribe(
      (data) => {
        console.log(data)
        // this.loading = false;
        data.forEach(
          (e) => {
            console.log(e.data())
            let data: any = e.data()
            data.id = e.id

            this.jobsProfiles.push(data)
            
            

          }
        )
      }
    )
    this.getUserDetails()
  }

  sortProfile(){
    console.log(this.jobAppliedUsers)
    this.jobAppliedUsers = _.orderBy(this.unFliteredJobAppledUser, "resumeValue", 'asc');
    console.log(this.jobAppliedUsers)
  }
  getUserDetails() {

    this.auth.authState

      .subscribe(
        (user) => {
          console.log(user)

          if (user) {
            this.userName = user.displayName

            const admins = ['thumusreerukmini9@gmail.com', 'ramkiransampathi@gmail.com', 'saicharitha905@gmail.com', 'tatanithin007@gmail.com', 'jaswanthtata@gmail.com']
            const userEmail = user.email
            console.log(admins.includes(userEmail))
            if (admins.includes(userEmail)) {

            } else {
              this.router.navigate(['jobs'])
            }

          } else {
            this.router.navigate(['home'])
          }


        }
      )
  }


  getJobAppliedUsers(item) {
    
    console.log(item.id)
    this.afs.collection('jobsApplied', ref => ref.where("id", "==", item.id)).get()
      .subscribe(
        (data) => {
          delete (this.userApplication);
          this.jobAppliedUsers = []
          this.unFliteredJobAppledUser = []
          data.forEach(
            (e) => {
              console.log(e.data())
              let data: any = e.data()
              data.id = e.id

              this.jobAppliedUsers.push(data)
              this.unFliteredJobAppledUser.push(data)
            }
          )
          // this.sortProfile()
        }

      )


  }
  getUserApplication(item) {
    this.userApplication = item


  }
}
