//ray0_bouton=12;  // diam 2.2
//ray1_bouton=10;  // diam 1.9
haut_bouton=20+1;
nb_crans=40;
ray_cran=1;
ray0_bouton=22/2-ray_cran;  // diam 2.2
ray1_bouton=19/2-ray_cran;  // diam 1.9
ray0_axe=11/2;
haut0_axe=haut_bouton/4*3;

$fn=36;

module Base_Bouton() {
  difference() {
    linear_extrude(height=haut_bouton,scale=ray1_bouton/ray0_bouton)
      union() {
        difference() {
          for (i=[0:360/nb_crans:359])
            translate([ray0_bouton*cos(i),ray0_bouton*sin(i)]) circle(ray_cran);
          circle(ray0_bouton-0.1);
        }
        circle(ray0_bouton);
      }
    translate([0,0,-0.1]) cylinder(r=ray0_axe+0.3,h=haut0_axe+0.1);
  }
}

/*
module Base_Bouton() {
  difference() {
    union()  {
      translate([0,0,-1]) cylinder(r1=ray0_bouton,r2=ray1_bouton,h=haut_bouton+1) ;
      for (i=[0:360/nb_crans:359]) {
        rotate([0,0,i]) {
          translate([ray1_bouton+(ray0_bouton-ray1_bouton)/2,0,haut_bouton/2])
            rotate([0,90+atan(haut_bouton/(ray0_bouton-ray1_bouton)),0])
              cylinder(r2=ray_cran,r1=ray_cran*ray1_bouton/ray0_bouton,h=haut_bouton+0.5,center=true);
          translate([ray1_bouton,0,haut_bouton]) sphere(ray_cran*ray1_bouton/ray0_bouton);
        }
      }
    }
   translate([0,0,-0.1]) cylinder(r=ray0_axe+0.3,h=haut0_axe+0.1);
  }
}
*/
//Bouton_Radio();

module Chapeau_Bouton() {
  translate([0,0,-2]) difference() {
    rotate_extrude() union() {
      square([ray1_bouton-1.5,4]);
      translate([ray1_bouton-1.5,2]) circle(2);
    }
    translate([-2*ray1_bouton,-2*ray1_bouton],0) cube([4*ray1_bouton,4*ray1_bouton,2]);
    translate([0,5.3,3.5]) cylinder(r=1,h=5);
  }
}

/*
ray_sphere=30;
haut_chapeau=4;
module Chapeau_Bouton() { // diam 1.3
  difference() {
    translate([0,0,-ray_sphere+haut_chapeau/2+2]) minkowski() {
      intersection() {
        sphere(30,$fn=72);
        translate([0,0,ray_sphere-haut_chapeau/2]) cylinder(r=ray1_bouton-2,h=haut_chapeau);
      }
      sphere(2);
    }
   translate([0,4.5,5.4]) cylinder(r=1,h=5);
  }
}
*/

module Bouton_Radio() {
  difference() {
    translate([0,0,-1]) union() {
      Base_Bouton();
      translate([0,0,haut_bouton-0.1]) Chapeau_Bouton();
    }
    translate([0,0,-2]) cube([50,50,4],center=true);
  }
}
  
Bouton_Radio();
//Chapeau_Bouton();
