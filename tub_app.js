/* TUB 雲端架構成本計算機 — JavaScript */
/* Taiwan United Bank · AWS Cost Calculator */

function revealTotal(){
  var el=document.getElementById('hdr-total');
  var btn=document.getElementById('reveal-btn');
  if(el.style.filter==='none'){
    el.style.filter='blur(10px)';
    btn.textContent='🔎 顯示金額';
    btn.classList.remove('revealed');
  } else {
    el.style.filter='none';
    btn.textContent='🔒 隱藏金額';
    btn.classList.add('revealed');
  }
}
function openArchModal(){
  var modal=document.getElementById('arch-modal');
  modal.classList.add('open');
}
function closeArchModal(event){
  if(event){
    event.stopPropagation();
  }
  var modal=document.getElementById('arch-modal');
  modal.classList.remove('open');
}
function toggleAnswer(id){
  var ans=document.getElementById(id+'-ans');
  var btn=document.querySelector('#'+id+' .quiz-toggle');
  if(ans.classList.contains('open')){ans.classList.remove('open');btn.textContent='顯示答案';}
  else{ans.classList.add('open');btn.textContent='隱藏答案';}
}
function switchTab(id,btn){
  document.querySelectorAll('.tab-btn').forEach(function(b){b.classList.remove('active');});
  document.querySelectorAll('.tab-content').forEach(function(c){c.classList.remove('active');});
  btn.classList.add('active');
  document.getElementById('tab-'+id).classList.add('active');
}
function showScenario(id,btn){
  document.querySelectorAll('.sc-tab').forEach(function(b){b.classList.remove('active');});
  document.querySelectorAll('.scenario-panel').forEach(function(p){p.classList.remove('active');});
  btn.classList.add('active');
  document.getElementById('sc-'+id).classList.add('active');
}
function toggleCostDetails(){
  var wrap=document.getElementById('cost-detail-wrap');
  var btn=document.getElementById('toggle-cost-btn');
  if(wrap.style.display==='none'){
    wrap.style.display='block';
    btn.textContent='隱藏表格';
  } else {
    wrap.style.display='none';
    btn.textContent='展開明細';
  }
}
function recalc(){
  var cfGb    = +document.getElementById('cf-gb').value    ||0;
  var albReq  = +document.getElementById('alb-req').value  ||0;
  var natGb   = +document.getElementById('nat-gb').value   ||0;
  var ec2Hr   = +document.getElementById('ec2-hr').value   ||0;
  var ebsGb   = +document.getElementById('ebs-gb').value   ||0;
  var auroraGb= +document.getElementById('aurora-gb').value||0;
  var s3Gb    = +document.getElementById('s3-gb').value    ||0;

  // 東京費率 ap-northeast-1
  var cf    = Math.round(cfGb * 0.120);
  var alb   = Math.round(5.76 + albReq * 0.22);
  var nat   = Math.round(0.045*720 + natGb*0.045 + 14.22);
  var ec2   = Math.round(0.0552 * ec2Hr * 30 * 2);
  var ebs   = Math.round(ebsGb * 0.096 * 2);
  var aurora= Math.round(0.3195*720*2 + auroraGb*0.10);
  var s3    = Math.round(s3Gb * 0.025);

  var wT=cf+alb+nat, aT=ec2+ebs, dT=aurora+s3, tot=wT+aT+dT;
  function f(n){return '$'+n.toLocaleString();}

  document.getElementById('cost-cf').textContent    =f(cf);
  document.getElementById('cost-alb').textContent   =f(alb);
  document.getElementById('cost-nat').textContent   =f(nat);
  document.getElementById('cost-ec2').textContent   =f(ec2);
  document.getElementById('cost-ebs').textContent   =f(ebs);
  document.getElementById('cost-aurora').textContent=f(aurora);
  document.getElementById('cost-s3').textContent    =f(s3);
  document.getElementById('badge-w').textContent    =f(wT);
  document.getElementById('badge-a').textContent    =f(aT);
  document.getElementById('badge-d').textContent    =f(dT);
  document.getElementById('sum-w').textContent      =f(wT);
  document.getElementById('sum-a').textContent      =f(aT);
  document.getElementById('sum-d').textContent      =f(dT);
  document.getElementById('panel-total').textContent=f(tot);
  document.getElementById('hdr-total').textContent  =f(tot);
  var mx=Math.max(wT,aT,dT,1);
  document.getElementById('bar-w').style.width=(wT/mx*100)+'%';
  document.getElementById('bar-a').style.width=(aT/mx*100)+'%';
  document.getElementById('bar-d').style.width=(dT/mx*100)+'%';
  document.getElementById('st-cf').textContent    =f(cf);
  document.getElementById('st-alb').textContent   =f(alb);
  document.getElementById('st-nat').textContent   =f(nat);
  document.getElementById('st-ec2').textContent   =f(ec2);
  document.getElementById('st-ebs').textContent   =f(ebs);
  document.getElementById('st-aurora').textContent=f(aurora);
  document.getElementById('st-s3').textContent    =f(s3);
  document.getElementById('st-total').textContent =f(tot);
}
recalc();