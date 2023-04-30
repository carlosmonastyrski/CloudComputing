resource "google_compute_instance" "web-server-1" {
  name         = "web-server-1"
  machine_type = "n1-standard-1"
  zone         = "europe-central2-a"
  tags         = ["http-server"]
  boot_disk {
    initialize_params {
      image = "debian-cloud/debian-10"
    }
  }

  network_interface {
    network = "default"
  }

  metadata_startup_script = "sudo apt-get update && sudo apt-get install -y apache2 && sudo service apache2 start"
}

resource "google_compute_instance" "web-server-2" {
  name         = "web-server-2"
  machine_type = "n1-standard-1"
  zone         = "europe-central2-a"
  tags         = ["http-server"]
  boot_disk {
    initialize_params {
      image = "debian-cloud/debian-10"
    }
  }

  network_interface {
    network = "default"
  }

  metadata_startup_script = "sudo apt-get update && sudo apt-get install -y apache2 && sudo service apache2 start"
}

resource "google_compute_firewall" "allow-http" {
  name    = "allow-http"
  network = "default"
  allow {
    protocol = "tcp"
    ports    = ["80"]
  }

  source_ranges = ["0.0.0.0/0"]
  target_tags   = ["http-server"]
}