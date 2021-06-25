import { Component, OnInit } from '@angular/core';
import { AngularFireAuth } from '@angular/fire/auth';
import { AngularFirestore } from '@angular/fire/firestore';
import { Router } from '@angular/router';

@Component({
  selector: 'app-admin',
  templateUrl: './admin.component.html',
  styleUrls: ['./admin.component.scss']
})
export class AdminComponent implements OnInit {
  userName = ""
  jobsProfiles = []
  constructor(private auth: AngularFireAuth, private router: Router, private afs: AngularFirestore,) { }

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

}
