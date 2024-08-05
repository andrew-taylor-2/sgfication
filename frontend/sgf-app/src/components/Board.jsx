import React, { useEffect, useState } from 'react';
import { Goban } from '@sabaki/shudan';
import '@sabaki/shudan/css/goban.css';
import sgf from '@sabaki/sgf'; // Import the SGF parser

const Board = ({ sgfData }) => {
  // let's make a default
  const defaultBoardSize = 19;
  const defaultSignMap = Array.from({ length: defaultBoardSize }, () => Array(defaultBoardSize).fill(0));

  const [signMap, setSignMap] = useState(defaultSignMap);
  const [vertexSize, setVertexSize] = useState(24);
  const [isBusy, setIsBusy] = useState(false);
  const [showCoordinates, setShowCoordinates] = useState(false);
  const [alternateCoordinates, setAlternateCoordinates] = useState(false);

  useEffect(() => {
    if (sgfData) {
      const parseSGF = (sgfData) => {
        const collection = sgf.parse(sgfData);
        const gameTree = collection[0];
        const rootNode = gameTree.data;
        const boardSize = parseInt(rootNode.SZ[0]);
        const signMap = Array.from({ length: boardSize }, () => Array(boardSize).fill(0)); // Initialize a 2D array with 0 (empty)

        const parseCoordinates = (coords) => {
          return coords.map(coord => {
            const x = coord.charCodeAt(0) - 97;
            const y = coord.charCodeAt(1) - 97;
            return [x, y];
          });
        };

        if (rootNode.AB) {
          parseCoordinates(rootNode.AB).forEach(([x, y]) => {
            signMap[y][x] = 1; // Black stones
          });
        }

        if (rootNode.AW) {
          parseCoordinates(rootNode.AW).forEach(([x, y]) => {
            signMap[y][x] = -1; // White stones
          });
        }

        return signMap;
      };

      const newSignMap = parseSGF(sgfData);
      setSignMap(newSignMap);
    }
  }, [sgfData]);

  return (
    <div>
      <section style={{ display: 'grid', gridTemplateColumns: '15em auto', gridColumnGap: '1em' }}>
        <form style={{ display: 'flex', flexDirection: 'column' }}>
          <p style={{ margin: '0 0 .5em 0' }}>
            Size:{' '}
            <button
              type="button"
              onClick={() => setVertexSize(Math.max(vertexSize - 4, 4))}
            >
              -
            </button>{' '}
            <button
              type="button"
              title="Reset"
              onClick={() => setVertexSize(24)}
            >
              •
            </button>{' '}
            <button
              type="button"
              onClick={() => setVertexSize(vertexSize + 4)}
            >
              +
            </button>
          </p>
          <p style={{ margin: '0 0 .5em 0' }}>
            Stones:{' '}
            <button
              type="button"
              title="Reset"
              onClick={() => setSignMap(defaultSignMap)}
            >
              •
            </button>
          </p>
          <label style={{ display: 'flex', alignItems: 'center' }}>
            <input
              style={{ marginRight: '.5em' }}
              type="checkbox"
              checked={showCoordinates}
              onClick={() => setShowCoordinates(!showCoordinates)}
            />
            <span style={{ userSelect: 'none' }}>Show coordinates</span>
          </label>
          <label style={{ display: 'flex', alignItems: 'center' }}>
            <input
              style={{ marginRight: '.5em' }}
              type="checkbox"
              checked={alternateCoordinates}
              onClick={() => setAlternateCoordinates(!alternateCoordinates)}
            />
            <span style={{ userSelect: 'none' }}>Alternate coordinates</span>
          </label>
          <label style={{ display: 'flex', alignItems: 'center' }}>
            <input
              style={{ marginRight: '.5em' }}
              type="checkbox"
              checked={isBusy}
              onClick={() => setIsBusy(!isBusy)}
            />
            <span style={{ userSelect: 'none' }}>Busy</span>
          </label>
        </form>
        <div>
          <Goban
            vertexSize={vertexSize}
            signMap={signMap}
            busy={isBusy}
            coordX={showCoordinates}
            coordY={showCoordinates}
            onVertexMouseUp={(evt, [x, y]) => {
              const sign = evt.button === 0 ? 1 : -1;
              const newSignMap = signMap.map((row, rowIndex) =>
                row.map((value, colIndex) => (rowIndex === y && colIndex === x ? sign : value))
              );
              setSignMap(newSignMap);
            }}
          />
        </div>
      </section>
    </div>
  );
};

export default Board;
