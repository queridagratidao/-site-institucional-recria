/* Recria · formulário de agendamento + questionário (Diagnóstico e Mentoria).
   Configuração na página: window.AGENDA = { API, produto: 'consultoria'|'mentoria', modos: ['video','whatsapp'], rotulo, zap }.
   Fala com o Apps Script apps-script-agenda.gs (chaves do questionário = CAMPOS do script). */
(function () {
  var C = window.AGENDA || {}, root = document.getElementById('ag-root');
  if (!root) return;
  var ZAP = C.zap || '5551991091697';
  var modos = C.modos || ['video'];
  var tz = 'America/Sao_Paulo';

  var PERGUNTAS = [
    { k: 'negocio', t: 'Nome do seu negócio', ob: 1, curta: 1 },
    { k: 'instagram', t: 'Instagram ou site do negócio', curta: 1, ph: '@seunegocio' },
    { k: 'cidade', t: 'Cidade e estado onde você atua', curta: 1 },
    { k: 'vende', t: 'O que você vende? Principais produtos ou serviços e os preços', ob: 1, ph: 'Ex.: corte feminino R$ 90, coloração R$ 250...' },
    { k: 'cliente', t: 'Quem é o seu cliente ideal?', ob: 1, ph: 'Quem compra de você hoje e quem você gostaria que comprasse?' },
    { k: 'vendas', t: 'Como as vendas acontecem hoje?', ob: 1, ph: 'Instagram, WhatsApp, indicação, loja física, site...' },
    { k: 'tempo', t: 'Há quanto tempo o negócio existe?', curta: 1 },
    { k: 'equipe', t: 'Quem trabalha no negócio hoje?', curta: 1, ph: 'Só eu, eu e mais 2 pessoas...' },
    { k: 'marketing', t: 'O que você faz hoje de conteúdo e anúncios?', ph: 'Posta quantas vezes? Investe em anúncios? Quanto?' },
    { k: 'dor', t: 'Qual é a maior dificuldade do seu negócio hoje?', ob: 1 },
    { k: 'tentou', t: 'O que você já tentou para resolver isso?' },
    { k: 'objetivo', t: 'Onde você quer chegar nos próximos 6 meses?', ob: 1 },
    { k: 'duvidas', t: 'Alguma dúvida ou algo que queira que eu veja com atenção? (opcional)' }
  ];

  var css = '.ag{max-width:680px;margin:0 auto;text-align:left;font-family:inherit}' +
    '.ag h3{font-family:"Playfair Display",serif;font-size:1.25rem;margin:26px 0 6px;color:#E4C988}' +
    '.ag p.ag-nota{font-size:15px;color:#b8ad96;margin:0 0 12px}' +
    '.ag label{display:flex;flex-direction:column;gap:6px;font-size:16px;margin-bottom:14px}' +
    '.ag input,.ag select,.ag textarea{width:100%;padding:14px 16px;border-radius:6px;border:1.5px solid rgba(201,162,78,.5);background:#fff;color:#2a2a2a;font-family:inherit;font-size:16px}' +
    '.ag textarea{min-height:84px;resize:vertical}' +
    '.ag input:focus,.ag select:focus,.ag textarea:focus{outline:2px solid #C9A24E}' +
    '.ag-modos{display:grid;gap:12px;margin:10px 0 6px}' +
    '.ag-modo{display:flex;flex-direction:row;gap:12px;align-items:flex-start;border:1.5px solid rgba(201,162,78,.45);border-radius:10px;padding:14px 16px;cursor:pointer;margin:0}' +
    '.ag-modo input{width:auto;margin-top:5px;accent-color:#C9A24E}' +
    '.ag-modo b{display:block;color:#E4C988}' +
    '.ag-modo span{font-size:15px;color:#cfcabf}' +
    '.ag-modo.on{background:rgba(201,162,78,.12);border-color:#C9A24E}' +
    '.ag-btn{display:block;width:100%;border:0;cursor:pointer;background:#C9A24E;color:#000;font-family:inherit;font-weight:700;font-size:17px;padding:16px;border-radius:6px;margin-top:8px}' +
    '.ag-btn:disabled{opacity:.6;cursor:wait}' +
    '.ag-msg{font-size:15px;margin-top:10px;min-height:20px;color:#E4C988}' +
    '.ag-ok{text-align:center;border:1px solid #C9A24E;border-radius:12px;padding:30px 22px;background:rgba(201,162,78,.08)}' +
    '.ag-ok h2{margin:0 0 10px}.ag-ok p{margin:0 0 14px}' +
    '.ag-zap{display:inline-block;background:#25D366;color:#000;font-weight:700;text-decoration:none;padding:14px 24px;border-radius:6px}';
  var st = document.createElement('style'); st.textContent = css; document.head.appendChild(st);

  function esc(s) { return String(s).replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; }); }
  function zapLink(t) { return 'https://wa.me/' + ZAP + '?text=' + encodeURIComponent(t); }
  function dia(d) { return new Date(d).toLocaleDateString('pt-BR', { timeZone: tz, weekday: 'long', day: '2-digit', month: '2-digit' }); }
  function hora(d) { return new Date(d).toLocaleTimeString('pt-BR', { timeZone: tz, hour: '2-digit', minute: '2-digit' }); }
  function chave(d) { return new Date(d).toLocaleDateString('en-CA', { timeZone: tz }); }

  if (!C.API) {
    root.innerHTML = '<div class="ag-ok"><h2>Agenda em instantes</h2><p>Estamos liberando a agenda. Enquanto isso, chame a Amanda no WhatsApp que ela combina com você.</p><a class="ag-zap" target="_blank" rel="noopener" href="' + zapLink('Oi, acabei de comprar o ' + (C.rotulo || 'produto') + ' e quero agendar') + '">Falar no WhatsApp</a></div>';
    return;
  }

  var h = '<form class="ag" id="ag-f" novalidate>';
  if (modos.length > 1) {
    h += '<h3>Como você prefere fazer?</h3><div class="ag-modos">' +
      '<label class="ag-modo on"><input type="radio" name="modo" value="video" checked><div><b>Por chamada de vídeo (1 hora)</b><span>Escolha o dia e o horário. Conversamos ao vivo e eu te envio o diagnóstico depois.</span></div></label>' +
      '<label class="ag-modo"><input type="radio" name="modo" value="whatsapp"><div><b>Sem chamada, por formulário e WhatsApp</b><span>Você responde o formulário, tiramos as dúvidas pelo WhatsApp e eu te entrego o diagnóstico em PDF.</span></div></label></div>';
  }
  h += '<h3>Seus dados</h3>' +
    '<label>Seu nome<input name="nome" required autocomplete="name"></label>' +
    '<label>WhatsApp com DDD<input name="whatsapp" required inputmode="tel" autocomplete="tel" placeholder="(51) 99999-9999"></label>' +
    '<label>E-mail (o convite do Google Meet vai para ele)<input name="email" type="email" required autocomplete="email"></label>' +
    '<div id="ag-hor"><h3>Escolha o dia e o horário</h3><p class="ag-nota" id="ag-hn">Carregando os horários...</p>' +
    '<label>Dia<select id="ag-dia"></select></label><label>Horário<select id="ag-hora"></select></label></div>' +
    '<h3>Conte um pouco sobre o seu negócio</h3><p class="ag-nota">Quanto mais você contar, mais direcionada fica a nossa conversa. Os campos com * são obrigatórios.</p>';
  PERGUNTAS.forEach(function (q) {
    h += '<label>' + esc(q.t) + (q.ob ? ' *' : '') + (q.curta ? '<input name="' + q.k + '"' : '<textarea name="' + q.k + '"') + (q.ph ? ' placeholder="' + esc(q.ph) + '"' : '') + (q.curta ? '>' : '></textarea>') + '</label>';
  });
  h += '<button class="ag-btn" type="submit" id="ag-ok">Enviar</button><p class="ag-msg" id="ag-msg"></p></form>';
  root.innerHTML = h;

  var F = document.getElementById('ag-f'), D = document.getElementById('ag-dia'), H = document.getElementById('ag-hora'),
      HN = document.getElementById('ag-hn'), HOR = document.getElementById('ag-hor'), BT = document.getElementById('ag-ok'),
      MSG = document.getElementById('ag-msg'), slots = {}, temSlots = false;

  function modoAtual() { var r = F.querySelector('input[name=modo]:checked'); return r ? r.value : 'video'; }
  function atualiza() {
    var m = modoAtual();
    Array.prototype.forEach.call(F.querySelectorAll('.ag-modo'), function (l) { l.className = 'ag-modo' + (l.querySelector('input').checked ? ' on' : ''); });
    HOR.style.display = m === 'video' ? 'block' : 'none';
    BT.textContent = m === 'video' ? 'Confirmar meu horário e enviar o formulário' : 'Enviar o formulário';
  }
  Array.prototype.forEach.call(F.querySelectorAll('input[name=modo]'), function (r) { r.addEventListener('change', atualiza); });
  atualiza();

  function horas() { H.innerHTML = ''; (slots[D.value] || []).forEach(function (s) { var o = document.createElement('option'); o.value = s.inicio; o.textContent = hora(s.inicio) + ' às ' + hora(s.fim); H.appendChild(o); }); }
  D.addEventListener('change', horas);

  fetch(C.API + '?acao=slots').then(function (r) { return r.json(); }).then(function (j) {
    if (!j.ok || !j.slots || !j.slots.length) throw new Error('vazio');
    j.slots.forEach(function (s) { var k = chave(s.inicio); (slots[k] = slots[k] || []).push(s); });
    Object.keys(slots).forEach(function (k) { var o = document.createElement('option'); o.value = k; o.textContent = dia(slots[k][0].inicio); D.appendChild(o); });
    horas(); temSlots = true; HN.textContent = 'Os horários já consideram a antecedência da minha agenda. Cada sessão dura 1 hora, por Google Meet.';
  }).catch(function () {
    HN.textContent = 'Não consegui carregar os horários agora. ' + (modos.length > 1 ? 'Escolha a opção sem chamada ou chame a Amanda no WhatsApp.' : 'Chame a Amanda no WhatsApp para combinarmos.');
  });

  F.addEventListener('submit', function (e) {
    e.preventDefault();
    var modo = modoAtual(), d = { acao: 'agendar', produto: C.produto, modo: modo, nome: F.nome.value.trim(), whatsapp: F.whatsapp.value.trim(), email: F.email.value.trim(), respostas: {} };
    if (!d.nome || !d.whatsapp || !d.email) { MSG.textContent = 'Preencha nome, WhatsApp e e-mail.'; return; }
    if (modo === 'video') { if (!temSlots || !H.value) { MSG.textContent = 'Escolha um dia e horário.'; return; } d.inicio = H.value; }
    for (var i = 0; i < PERGUNTAS.length; i++) {
      var q = PERGUNTAS[i], v = F.elements[q.k].value.trim(); d.respostas[q.k] = v;
      if (q.ob && v.length < 2) { MSG.textContent = 'Responda: ' + q.t + '.'; F.elements[q.k].focus(); return; }
    }
    BT.disabled = true; MSG.textContent = 'Enviando...';
    fetch(C.API, { method: 'POST', headers: { 'Content-Type': 'text/plain;charset=utf-8' }, body: JSON.stringify(d) })
      .then(function (r) { return r.json(); }).then(function (j) {
        if (!j.ok) { MSG.textContent = (j.erro || 'Não foi possível enviar.') + ' Tente de novo ou chame a Amanda no WhatsApp.'; BT.disabled = false; return; }
        if (typeof fbq !== 'undefined') { try { fbq('track', 'Schedule'); } catch (x) {} }
        var msgZap = 'Oi, sou ' + d.nome + '. Acabei de enviar o formulário do ' + (C.rotulo || 'produto') + '.';
        if (modo === 'video') {
          root.innerHTML = '<div class="ag-ok"><h2>Tudo certo!</h2><p>Seu horário está marcado para <b>' + dia(d.inicio) + ' às ' + hora(d.inicio) + '</b>.</p><p>O convite com o link do Google Meet foi enviado para <b>' + esc(d.email) + '</b> (olhe o spam se não aparecer). Já recebi as suas respostas e vou chegar na chamada preparada.</p><a class="ag-zap" target="_blank" rel="noopener" href="' + zapLink(msgZap) + '">Falar no WhatsApp</a></div>';
        } else {
          root.innerHTML = '<div class="ag-ok"><h2>Formulário recebido!</h2><p>Agora o próximo passo é a nossa conversa pelo WhatsApp. Chame a Amanda para tirarmos as dúvidas, e depois eu te entrego o seu diagnóstico em PDF.</p><a class="ag-zap" target="_blank" rel="noopener" href="' + zapLink(msgZap) + '">Continuar no WhatsApp</a></div>';
        }
        root.scrollIntoView({ behavior: 'smooth', block: 'start' });
      }).catch(function () { MSG.textContent = 'Falha de conexão. Tente de novo ou chame a Amanda no WhatsApp.'; BT.disabled = false; });
  });
})();
