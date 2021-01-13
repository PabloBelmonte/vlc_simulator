% =========================================================================
%                                                                         %
%          ******   C�digo Sistema com modula��o OFDM     *******         %
%                                                                         %
%         --------    Objetivo: Coopera��o com IT-IST    --------         %
%                                                                         %
%                                                                         %
% by Jair Silva                                                           %
% (LabTel/PPGEE/UFES)                                                     %
%  Outubro/2017                                 5                         %
% =========================================================================

% Inicializa��o
clc, clear all, close all,

pkg load communications

% ............... Parametros do Setup Expeimental ........................
pe.fs    = 40e6;                % Taxa de Amostragem do AD/DA
pe.Bw    = pe.fs/2;             % M�xima largura de banda --> Taxa Nyquist

% ..... Parametros de entrada (Padr�o ADSL Full Rate Downstream) .........
pe.Nfft  = 512;                 % Pontos da IFFT/FFT (numero de subportadoras)
pe.Ns    = 200;                 % Qtd Subportadoras de dados
pe.Ng    = 32;                  % Qtd de amostras do Prefixo C�clico (IG)
pe.IG    = round(pe.Ng/pe.Nfft);% Fator do intervalo de guarda IG

% ..... Parametros Calculados para a implementa��o .......................
pe.N     = (pe.Nfft - 2)/2;     % Qtd Subportadoras considerando Hermitiana
pe.NsH   = 2*pe.Ns + 2;         % Qtd de subportadoras ap�s Hermitiana
pe.Nz    = pe.Nfft - pe.NsH;    % Qtd subportadoras zeradas (zero padding)
pe.Mod   = [4 16 64 256];                   % �ndice de modula��o --> Escolhido
pe.n     = log2(pe.Mod);          % Qtd de bits por subportadora
pe.frame = 400;                   % Qtd de s�mbolos OFDM no frame - Escolhido
EbNo_dB  = 0:25;
BER_sim = zeros(length(pe.Mod),length(EbNo_dB));
% .................. Transmissor OFDM  ...................................
for(x=1:length(pe.Mod))
    % Gera��o dos dados
    % Dadostx = randint(pe.Ns,pe.frame,pe.Mod(x));  % devolve matriz de inteiros 200x10 com inteiros de 0 a Q-QAM
	Dadostx = randi(pe.Mod(x),pe.Ns,pe.frame)-1;
    
    % Modula��o QAM (Mapeamento)
    DadosModtx = qammod(Dadostx,pe.Mod(x));
    
    % Simetria Hermitiana --> antes da centraliza��o do espectro
    Hermit_tx = [zeros(1,pe.frame); DadosModtx; zeros(1,pe.frame); conj(flipud(DadosModtx))];
    
    % Zero padding --> Centraliza o espectro (realiza simetria hermitiana para que o output da IFFT seja um sinal real puro)
    pe.TH = length(Hermit_tx);
    info_tx = zeros(pe.Nfft,pe.frame);
    info_tx(1:pe.TH/2,:) = Hermit_tx(1:end/2,:);
    info_tx(end-(pe.TH/2-1):end,:) = Hermit_tx(end/2+1:end,:);
    
    % "Modula��o" via IDFT (ifft)
    ofdm_symbol_tx = ifft(info_tx,pe.Nfft);
    
    % Intervalo de Guarda
    ofdm_symbol_ig = [ofdm_symbol_tx(end+1-pe.Ng:end,:); ofdm_symbol_tx];
    
    % convers�o paralelo-s�rie
    ofdm_signal = reshape(ofdm_symbol_ig,1,pe.frame*length(ofdm_symbol_ig));
    
    % Normaliza o sinal
    pe.fat_norm = (max(ofdm_signal));
    ofdm_signal = ofdm_signal./pe.fat_norm;
    
    % Calcula a pot�ncia do sinal OFDM gerado
    potw = sum(ofdm_signal.*conj(ofdm_signal))/length(ofdm_signal);
    pe.pot = 10*log10(potw/1e-3); % em dBm
    
    % Calcula o PAPR do sinal OFDM gerado
    num = max(abs(ofdm_signal));
    den = mean(abs(ofdm_signal));
    pe.PAPR = 20*log10(num/den);
    
    
    % .........  Gera vetores tempo e frequencia .............................
    t = 0:1/pe.fs:((length(ofdm_signal)-1)/pe.fs);
    Twin = length(ofdm_signal)/pe.fs; % periodo de cada simbolo
    deltaf = 1/Twin; % intervalo de frequencia de cada subportadora
    fpos = 0 : deltaf : ((length(ofdm_signal)/2)-1)*deltaf;
    fneg = -(length(ofdm_signal)/2)*deltaf : deltaf : -deltaf;
    f = [fpos fneg];
    
    % .................. Plota Gr�ficos do Transmissor .......................
    % OFDM_SIGNAL_TX = graficos(DadosModtx(:,4:end),ofdm_signal,t,f,20,'b.','b');
    
    for(i=1:length(EbNo_dB))
        pe.snr(i) = EbNo_dB(i) + 10*log10(pe.NsH/pe.Nfft) + 10*log10(pe.n(x)); %10*log10(pe.Nfft/(pe.Nfft+pe.Ng));
        
        %  ###############  Exemplo de Canal de Comunica��o #####################
        
        % % Gera o perfil de pot�ncia do canal (taps no dom�nio do tempo)
        % h = [(randn+j*randn) (randn+j*randn)/2 (randn+j*randn)/4];
        %
        % % Convolu��o com o canal
        % ofdm_signal_noise = conv(ofdm_signal, h);
        %
        % % Retira as amostras excedentes devido � convolu��o
        % ofdm_signal_noise = ofdm_signal_noise(1:length(ofdm_signal));
        
        % % Insere Ru�do AWGN
        % ofdm_signal_noise = awgn(ofdm_signal_noise,pe.snr,'measured');
        %
        % % ofdm_signal_noise = ofdm_signal;  % B2B
        ofdm_signal_noise = awgn(ofdm_signal,pe.snr(i),'measured');
        
        % #########################################################################
        
        % ..................... Receptor OFDM  ...................................
        
        % Retira a normaliza��o
        ofdm_signal_rx = ofdm_signal_noise.*pe.fat_norm;
        
        % Convers�o serie - Paralelo (Matriz de sinais OFDM)
        ofdm_signal_rx = reshape(ofdm_signal_rx,length(ofdm_signal_rx)/pe.frame,pe.frame);
        
        % Retira o Intervalo de Guarda (IG)
        ofdm_symbol_rx = ofdm_signal_rx(pe.Ng+1:end,:);
        
        % Desmodula��o via DFT (fft)
        info_rx = fft(ofdm_symbol_rx,pe.Nfft);
        
        % Reconhecimento do Canal
        HH = info_rx(:,1:3)./info_tx(:,1:3);  % Coeficientes do Equalizador
        H = (mean(HH.')).';
        [lin,col] = size(info_rx);
        HH = repmat(H,1,col);
        
        % Equaliza��o via one-tap equalizer (Zero forcing)
%         info_rx = info_rx./HH;
        
        % Desfaz o zero padding
        Hermit_rx = [info_rx(1:pe.Ns+1,:); info_rx(end-pe.Ns:end,:)];
        
        % Remove a simetria Hermitiana
        DadosModrx = Hermit_rx(2:pe.Ns+1,:);
        
        % Detec��o
        Dadosrx = qamdemod(DadosModrx,pe.Mod(x));
        
        % Calcula a BER
        % BER = round(mean(mean(abs(Dadosrx(:,4:end)-Dadostx(:,4:end)))));
        [erros,BER_sim(x,i)] = biterr(Dadosrx(:,4:end),Dadostx(:,4:end));
    end
    
    % .................. Plota Gr�ficos do Receptor ..........................
    % OFDM_SIGNAL_RX = graficos(DadosModrx(:,4:end),ofdm_signal_noise,t,f,20,'r.','r');
    
    % .................. Plota Gr�ficos do Canal .............................
    
    % Resposta em frequencia do canal gerado
    % Tamh  = length(h);
    % Hg    = fft(h,length(ofdm_signal_noise));
    % Hg    = Hg./max(Hg);
    % Hg_dB = 10*log10(abs(Hg.*conj(Hg))); % Resposta de Amplitude (dB)
    %
    % % Resposta em frequencia do canal estimado
    % H_dB  = 10*log10(abs(H.*conj(H))); % Resposta de Amplitude (dB)
    % tamff = length(f)-length(H_dB);
    % ffi   = fftshift(f);
    % fff   = (ffi(tamff/2:end-tamff/2-1))';
    %
    % figure
    % subplot(2,1,1), plot(fftshift(f),fftshift(Hg_dB),'b'); grid on;
    % title('Resposta Freq. Gerada'); xlabel('Freq. [Hz]'); ylabel('|H| [dB/Hz]');
    %
    % subplot(2,1,2), plot(fff,fftshift(H_dB),'r:+','Markersize',4); grid on
    % title('Resposta Freq. Estimada'); xlabel('Freq. [Hz]'); ylabel('|H| [dB/Hz]');
    
    
    % ..... Parametros Calculados para Informes ..............................
    pe.DF    = pe.Bw/pe.N;              % Espa�amento em freq. entre subport.
    pe.Bwe   = pe.Ns*pe.DF;             % Largura de banda efetiva
    pe.Rb    = (pe.DF*pe.Ns*pe.n)/(1+pe.IG);  % Taxa de transmiss�o REAL
    pe.Tu    = 1/pe.DF;                 % Dura��o �til do sinal OFDM
    pe.Tg    = pe.Ng*(1/pe.fs);         % Dura��o do intervalo de guarda (CP)
    pe.Ts    = pe.Tu + pe.Tg;           % Dura��o total sinal OFDM ( = t(end))
    pe.Perda = 10*log10(1-pe.Tg/pe.Ts); % Perda gerada pela inser��o do IG.
    
    % ......................... Comandos de Sa�da ............................
    disp ('                                                                 ');
    disp ('=================================================================');
    disp ('  Prinicpais Par�metros do Sistema com Modula��o OFDM            ');
    disp ('=================================================================');
    disp ('                                                                 ');
    fprintf(' Taxa de amotragem [Sps]              : %0.7g \n',pe.fs);
    fprintf(' Largura de Banda Total [Hz]          : %0.7g \n',pe.Bw);
    fprintf(' Taxa de Transfer�ncia [bps]          : %0.7g \n',pe.Rb);
    fprintf(' Largura de Banda [Hz]                : %0.7g \n',pe.Bwe);
    fprintf(' Subportadoras de Informa��o          : %0.7g \n',pe.Ns);
    fprintf(' Espa�amento entre Subportadoras [Hz] : %0.7g \n',pe.DF);
    fprintf(' N�vel de Modula��o por Subportadora  : %0.7g QAM \n',pe.Mod(x));
    fprintf(' Quantidade de Pontos da IFFT/FFT     : %0.7g \n',pe.Nfft);
    fprintf(' Dura��o Total do S�mbolo OFDM [s]    : %0.7g \n',pe.Ts);
    fprintf(' Dura��o �til do S�mbolo OFDM [s]     : %0.7g \n',pe.Tu);
    fprintf(' Dura��o do Intervalo de Guarda [s]   : %0.7g \n',pe.Tg);
    fprintf(' Perda SNR por inser��o do IG [dB]    : %0.7g \n',pe.Perda);
    fprintf(' Potencia Sinal OFDM [dBm]            : %0.7g \n',pe.pot);
    fprintf(' PAPR Raz�o Pot. M�x. e Pot M�d. [dB] : %0.7g \n',pe.PAPR);
    fprintf(' Taxe de Erro de Bits BER             : %0.7g \n',BER_sim);
    disp ('                                                                 ');
    disp ('=================================================================');
end

% Figura de BER em fun��o de SNR
figure
semilogy(EbNo_dB,BER_sim,'o');
xlabel('Eb/No (dB)');
ylabel('BER');

% BER Te�rico
for kk = 1:length(pe.Mod)
    for jj = 1:length(EbNo_dB)
        EbNo_teorico = EbNo_dB(jj);
        ber_awgn_teorico(jj) = berawgn(EbNo_teorico, 'qam', pe.Mod(kk));
    end
    hold all
    semilogy(EbNo_dB,ber_awgn_teorico,'-')
    grid on;
    ber_awgn_teorico_mat(kk,:) = ber_awgn_teorico;
end
axis([0 EbNo_dB(end) 1e-5 1e0])
legend('4-QAM Simulado','16-QAM Simulado','64-QAM Simulado','256-QAM Simulado',...
       '4-QAM Te�rico','16-QAM Te�rico','64-QAM Te�rico', '256-QAM Te�rico');
%