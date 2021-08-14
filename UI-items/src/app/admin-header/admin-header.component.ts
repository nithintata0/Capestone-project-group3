import { Component, OnInit } from '@angular/core';
import { AngularFireAuth } from '@angular/fire/auth';
import { Router } from '@angular/router';

@Component({
  selector: 'app-admin-header',
  templateUrl: './admin-header.component.html',
  styleUrls: ['./admin-header.component.scss']
})
export class AdminHeaderComponent implements OnInit {
  userName = ""

  visible:boolean = false
  constructor(
    private auth:AngularFireAuth,
    private router:Router
  ) { }

  ngOnInit(): void {
    this.auth.authState

    .subscribe(
      (user) => {
        console.log(user)

        if (user) {
          this.userName = user.displayName

          // const admins = ['thumusreerukmini9@gmail.com', 'ramkiransampathi@gmail.com', 'saicharitha905@gmail.com', 'tatanithin007@gmail.com', 'jaswanthtata@gmail.com']
          const userEmail = user.email
          // console.log(admins.includes(userEmail))
          // if (admins.includes(userEmail)) {

          // } else {
          //   this.router.navigate(['jobs'])
          // }
        
        } else {
          this.router.navigate(['home'])
        }


      }
    )
  }

  
}
