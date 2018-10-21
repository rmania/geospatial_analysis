--example 2: restaurants
[bbox:{{bbox}}];
( node["amenity"="restaurant"];
  way["amenity"="restaurant"];
  relation["amenity"="restaurant"]; );
out center;

--example 2: bridges
*/
[out:json][timeout:25];
// gather results
(
  // query part for: “bridge”
  way["man_made"="bridge"]({{bbox}});
  relation["man_made"="bridge"]({{bbox}});
);
// print results
out body;
>;
out skel qt;


--example 3 highway around schools with inappropriate maxspeed 
[out:json][timeout:800];

// Get all schools in current bounding box
( way[amenity=school]({{bbox}});
  node[amenity=school]({{bbox}});
  rel[amenity=school]({{bbox}});
)->.schools;

// find highway=* around schools with radius 50m, ignoring
// footway and paths. In addition, highways are relevant if they 
// either
// (1) have no maxspeed tag at all
// (2) maxspeed tag indicates a value larger than 30 km/h

way(around.schools:50)[highway][highway!~"^(footway|path)$"]
   (if: (is_number(t["maxspeed"]) && t["maxspeed"] > 30) || 
        !is_tag("maxspeed") )->.streets;

// get schools in 50m distance for all identified relevant streets
( node.schools(around.streets:50);
  way.schools(around.streets:50);
  rel.schools(around.streets:50);
 )->.matchingSchools;

// return results, schools and streets
(.matchingSchools; .streets;);
out geom;


-- Find banks where the closest police station is more than 500m away.
[out:json][bbox:{{bbox}}][timeout:800];

// determine set of police stations
(
  node[amenity=police];
  way[amenity=police];
  rel[amenity=police];
)->.polices; // put them into the set "polices"
 
// determine set of banks
(
  node[amenity=bank];
  way[amenity=bank];
  rel[amenity=bank];
)->.banks; // put them into the set "banks"
  
// determine set of banks near police stations
(
  node.banks(around.polices:500);
  way.banks(around.polices:500);
  rel.banks(around.polices:500);
)->.banksNearPolices; // put them into the set "banksNearPolices"

// determine banks far from police stations
(.banks; - .banksNearPolices;);

// return node, ways, relations as determined above
out geom meta;