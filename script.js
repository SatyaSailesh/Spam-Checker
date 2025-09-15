// Smooth scroll function
function scrollToSection(id){
  document.getElementById(id).scrollIntoView({behavior:'smooth'});
}

// Demo Simulation
function simulateDemo(){
  const msg = document.getElementById('messageInput').value;
  const res = Math.random() > 0.5 ? 'Spam ✅' : 'Not Spam 🚀';
  const conf = (Math.random()*20 + 80).toFixed(1);
  document.getElementById('demoResult').innerText = `${res} — Confidence: ${conf}%`;
}

// Modal Controls
function closeModal(){
  document.getElementById('modalBackdrop').style.display='none';
}

// Example: Dynamically add simple nodes to SVG
const svg = document.getElementById('pipeline');

const nodes = [
  {x:40,y:110,label:"Frontend UI"},
  {x:360,y:110,label:"Flask API"},
  {x:700,y:110,label:"Preprocessing"},
  {x:1000,y:110,label:"ML Model"},
  {x:1250,y:110,label:"Output"}
];

nodes.forEach(n=>{
  const g = document.createElementNS("http://www.w3.org/2000/svg","g");
  g.setAttribute("transform",`translate(${n.x},${n.y})`);
  
  const rect = document.createElementNS("http://www.w3.org/2000/svg","rect");
  rect.setAttribute("width",220);
  rect.setAttribute("height",120);
  rect.setAttribute("rx",16);
  rect.setAttribute("fill","rgba(255,255,255,0.02)");
  rect.setAttribute("stroke","#00d1ff");
  rect.setAttribute("stroke-width","1.5");
  
  const text = document.createElementNS("http://www.w3.org/2000/svg","text");
  text.setAttribute("x",12);
  text.setAttribute("y",24);
  text.setAttribute("fill","#dff7ff");
  text.setAttribute("font-size",16);
  text.setAttribute("font-weight",700);
  text.textContent = n.label;
  
  g.appendChild(rect);
  g.appendChild(text);
  svg.appendChild(g);
});
