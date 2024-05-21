
import React, { useEffect } from 'react';
import '../../public/wgo/wgo.player.css'; 

const Board = () => {
  useEffect(() => {
    const loadScript = (src) => {
      return new Promise((resolve, reject) => {
        const script = document.createElement('script');
        script.src = src;
        script.onload = resolve;
        script.onerror = reject;
        document.head.appendChild(script);
      });
    };

    const loadWGoScripts = async () => {
      const scripts = [
        '../../public/wgo/wgo.js',
        '../../public/wgo/kifu.js',
        '../../public/wgo/sgfparser.js',
        '../../public/wgo/player.js',
        '../../public/wgo/basicplayer.js',
        '../../public/wgo/basicplayer.component.js',
        '../../public/wgo/basicplayer.infobox.js',
        '../../public/wgo/basicplayer.commentbox.js',
        '../../public/wgo/basicplayer.control.js',
        '../../public/wgo/player.editable.js',
        '../../public/wgo/scoremode.js',
        '../../public/wgo/player.permalink.js'
      ];

      for (const src of scripts) {
        await loadScript(src);
      }

      // Initialize the WGo player
      new WGo.BasicPlayer(document.getElementById('board'), {
        sgf: "(;FF[4]AB[bh][bi][bk][bp][bq][ch][ck][cp][di][dj][dk][dp][ek][em][en][eo][es][ff][fg][fm][fq][fr][ga][gk][gl][go][gp][ha][hb][hc][hf][hg][hk][ho][hq][ic][id][ig][ih][ii][ij][ik][il][im][ip][iq][jd][jj][jl][jr][ka][kb][ki][km][kr][lb][lc][le][li][ll][mc][ml][mm][mr][ni][nl][no][nr][ob][oc][oi][oj][ok][oo][op][oq][or][pd][pk][pp][qc][qe][qi][ql][qo][re][ro]AW[bg][br][ce][cg][ci][cj][cq][dc][dh][dq][eb][eh][ei][ej][ep][eq][er][fa][fh][fj][fk][fl][fn][fo][fp][gb][gc][gd][gf][gg][gj][gm][gn][hd][he][hh][hi][hj][hl][hm][hn][if][in][io][jb][jf][jg][jh][ji][jm][jn][jo][jp][kj][kk][kl][kq][la][lk][lq][lr][ls][ma][mb][mk][mn][mo][nb][nc][nd][nf][nj][nk][nm][nn][np][nq][od][ol][on][pe][pf][pl][pn][po][qf][qn][rf][rn]CA[UTF-8]GM[1]SZ[19])",
        // "(;FF[4]GM[1]SZ[19]CA[UTF-8]SO[gokifu.com]BC[cn]WC[cn]PB[Gu Li]BR[9p]PW[Shi Yue]WR[5p]KM[7.5]DT[2012-10-21]RE[B+R];B[qd];W[dd];B[pq];W[dq];B[fc];W[cf];B[kc];W[qn];B[qp];W[pj];B[qh];W[on];B[pm];W[pn];B[mq];W[od];B[pf];W[qc];B[rc];W[of];B[og];W[pc];B[qk];W[pk];B[qj];W[ql];B[nf];W[rb];B[rd];W[mc];B[do];W[co];B[dp];W[cp];B[eq];W[cn];B[dr];W[cq];B[fp];W[dn];B[fn];W[jp];B[mo];W[gq];B[ho];W[iq];B[jn];W[lp];B[lq];W[kn];B[nm];W[om];B[km];W[in];B[io];W[jo];B[jm];W[lo];B[mp];W[lm];B[ll];W[kq];B[mm];W[ln];B[nk];W[qi];B[ri];W[pi];B[rj];W[op];B[oq];W[ok];B[el];W[dk];B[fj];W[dl];B[rl];W[nj];B[rm];W[mk];B[nl];W[qm];B[kk];W[ph];B[pg];W[mi];B[dg];W[df];B[db];W[eg];B[ei];W[eb];B[fb];W[cb];B[dc];W[cc];B[ed];W[da];B[ec];W[di];B[cd];W[bd];B[de];W[ce];B[dj];W[dh];B[fr];W[gr];B[cj];W[ek];B[ej];W[fk];B[gk];W[gl];B[hk];W[hl];B[il];W[hm];B[im];W[gp];B[fo];W[em];B[hn];W[ic];B[mb];W[nb];B[md];W[lb];B[lc];W[ma];B[kb];W[gg];B[ff];W[fg];B[gi];W[he];B[hd];W[id];B[ie];W[je];B[if];W[jf];B[hf];W[hc];B[nc];W[mb];B[nd];W[gd];B[gf];W[fe];B[ob];W[oc];B[pb];W[oa];B[ee];W[ef];B[ig];W[jg];B[ih];W[qb];B[jd];W[gb];B[jc];W[gc];B[ge];W[fd];B[ea];W[ca];B[ib];W[ga];B[hb];W[fa];B[ha];W[eb];B[kr];W[jr];B[ea];W[rh];B[hd];W[];B[tt])",
      });
    };

    loadWGoScripts();
  }, []);

  return (
    <div>
      <h1>WGo.js Player Demo</h1>
      <div id="board" style={{ width: '150%', margin: '0 auto' }}>
        Your browser doesn't support WGo Player. Use a modern browser like IE9, Google Chrome, or Mozilla Firefox.
      </div>
    </div>
  );
};

export default Board;
