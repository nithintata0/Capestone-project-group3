import { Component, Input, OnInit } from '@angular/core';
import { AngularFirestore, AngularFirestoreCollection } from '@angular/fire/firestore';
import { Observable } from 'rxjs';
import { AngularFireStorage } from '@angular/fire/storage';
import { AngularFireAuth } from '@angular/fire/auth';
import { Router } from '@angular/router';
import * as firebase from 'firebase';

@Component({
  selector: 'app-show-jobs',
  templateUrl: './show-jobs.component.html',
  styleUrls: ['./show-jobs.component.scss']
})
export class ShowJobsComponent implements OnInit {

  @Input() showController;
  loading = true;
  jobsProfiles = []
  userJobProfile = []
  userName = ""

  showJD: any
  constructor(private afs: AngularFirestore,
    private router: Router,
    private storage: AngularFireStorage, private auth: AngularFireAuth) { }

  ngOnInit(): void {


    this.jobsProfiles = []
    this.afs.collection('jobs').get().subscribe(
      (data) => {
        console.log(data)
        this.loading = false;
        data.forEach(
          (e) => {
            console.log(e.data())
            let data: any = e.data()
            data.id = e.id

            this.jobsProfiles.push(data)

          }
        )
        this.showJD = this.jobsProfiles[0]
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

            this.afs.collection("userProfiles").doc(user.uid).get().subscribe(
              (data) => {
                console.log(data.data())
                if (data.data()) {
                  this.userJobProfile = data.data()['userJobProfile']
                }

              }
            )
          } else {
            this.router.navigate(['home'])
          }


        }
      )
  }
  processFile(event, data) {
    this.auth.currentUser.then(
      (user) => {
        console.log(user.displayName)
        console.log(user.uid)
        console.log(data.id)
        const file = event.target.files[0];
        console.log(file.name)
        let filePath = data.id + "/" + user.displayName + file.userName
        filePath = filePath.replace(" ","_")
        const ref = this.storage.ref(filePath);
        const task = ref.put(file).then(

          async (uploadDtata) => {


            console.log(uploadDtata.metadata.fullPath)
            console.log("https://firebasestorage.googleapis.com/v0/b/capestone-945f7.appspot.com/o/" + uploadDtata.metadata.fullPath.replace('/', "%2F") + "?alt=media")
            console.log(uploadDtata)
            const getDownloadUrl = await ref.getDownloadURL().toPromise()


            this.afs.collection("jobsApplied").add(
              {
                id: user.uid,
                userName: user.displayName,
                ...data,
                date: Date(),
                url: getDownloadUrl
              }
            )
            this.userJobProfile.push(data.id)
            this.afs.collection("userProfiles").doc(user.uid).set({
              userJobProfile: this.userJobProfile
            }
            )
          }
        );
      }
    )



  }

  changeJD(item) {
    this.showJD = item;
  }

  goToEdit(id) {
    this.router.navigate(['add-jobs'], {
      queryParams: {
        id: id
      }
    })
  }
  deleteIt(id) {
    if (confirm(id)) {
      this.afs.collection("jobs").doc(id).delete().then(
        (doc) => {
          this.ngOnInit()
        }
      )
    }

  }
}
