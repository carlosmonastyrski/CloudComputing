provider "google" {
  credentials = "${file("account.json")}"
  project      = "agile-alignment-384815"
  region       = "europe-central2"
}