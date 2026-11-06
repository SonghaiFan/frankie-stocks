// Unsaved explanatory diagram: app return formula + actual four-band thresholds.
// Synthetic data, no network, storage or investment signal. Straight-segment paths
// simplify HorizonRow.tsx's curveMonotoneX rendering while preserving band values.
const data=JSON.parse(document.querySelector('#demo-data').textContent);
const svg=document.querySelector('#chart-example'),bench=document.querySelector('#benchmark'),bands=document.querySelector('#bands');
const changes=xs=>xs.map(x=>(x-xs[0])/xs[0]*100);
function render(){
 const raw=changes(data.prices),comparison=changes(data.benchmark),values=raw.map((v,i)=>v-(bench.checked?comparison[i]:0));
 const max=Math.max(...values.map(Math.abs),1),limits=(bands.value==='fibonacci'?data.ratios:[0,.25,.5,.75,1]).map(r=>r*max);
 const paths=[];
 for(const sign of [1,-1])for(let band=0;band<4;band++){
  const step=limits[band+1]-limits[band];const pts=values.map((v,i)=>{const h=Math.min(step,Math.max(0,Math.max(0,sign*v)-limits[band]))/step*70;return [i/(values.length-1)*500,sign>0?70-h:h];});
  const baseline=sign>0?70:0;const node=document.createElementNS('http://www.w3.org/2000/svg','path');node.setAttribute('d',`M0,${baseline} L${pts.map(p=>p.join(',')).join(' L')} L500,${baseline} Z`);node.setAttribute('fill',sign>0?'var(--pos)':'var(--neg)');node.setAttribute('fill-opacity',.18+.5*(band+1)/4);paths.push(node);
 }
 svg.replaceChildren(...paths);const last=values.at(-1);document.querySelector('#result').textContent=`${bench.checked?data.excess:data.return}: +${Math.round(last)}${bench.checked?' '+data.points:'%'}`;
}
bench.addEventListener('change',render);bands.addEventListener('change',render);render();
