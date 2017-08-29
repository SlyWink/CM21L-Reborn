haut0_bouton=2;
haut1_bouton=18-haut0_bouton+1;
haut2_bouton=2;
nb_crans=24;
ray_cran=2;
ray1_bouton=24/2-ray_cran;  // diam 2.2
ray0_bouton=ray1_bouton+ray_cran+2;
ray2_bouton=ray1_bouton-3/2;  // diam 1.9
ray0_axe=11/2;
haut0_axe=(haut1_bouton+haut0_bouton)/4*3;
ray_encoche=3/2;
$fn=36;

module Corps_Bouton() {
  linear_extrude(height=haut1_bouton,scale=ray2_bouton/ray1_bouton)
    union() {
      difference() {
        for (i=[0:360/nb_crans:359])
          translate([ray1_bouton*cos(i),ray1_bouton*sin(i)]) circle(ray_cran);
        circle(ray1_bouton-0.1);
      }
      circle(ray1_bouton);
    }
}


module Chapeau_Bouton() {
  translate([0,0,-haut2_bouton]) difference() {
    rotate_extrude() union() {
      square([ray2_bouton-0.5,haut2_bouton*2]);
      translate([ray2_bouton-0.5,haut2_bouton]) circle(haut2_bouton);
    }
    translate([-2*ray2_bouton,-2*ray2_bouton],0) cube([4*ray2_bouton,4*ray2_bouton,2]);
  }
}


module Base_Bouton() {
  difference() {
    cylinder(r=ray0_bouton,h=haut0_bouton);
    translate([ray0_bouton,0,-0.1]) cylinder(r=ray_encoche,h=haut0_bouton+0.2);
  }
}


module Bouton_Radio() {
  difference() {
    union() {
      Base_Bouton();  
      translate([0,0,haut0_bouton-0.1]) Corps_Bouton();
      translate([0,0,haut1_bouton+haut0_bouton-0.1]) Chapeau_Bouton();
    }
    translate([0,0,-0.1]) cylinder(r=ray0_axe+0.3,h=haut0_axe+0.1);
  }
}
  
Bouton_Radio();