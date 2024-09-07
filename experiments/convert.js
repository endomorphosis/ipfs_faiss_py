import os from 'os';
import fs from 'fs';
import path from 'path';

export function convert(ipfs_output_path){
    const ingest_ipfs_add_output = fs.readFileSync(ipfs_output_path, 'utf8');
    const ingest_ipfs_rows = [];

    for (const line of ingest_ipfs_add_output.split(os.EOL)) {
        const column_tabs = line.split('\t');
        const column_spaces = line.split(' ');
        const columns = column_tabs.length > column_spaces.length ? column_tabs : column_spaces;
        let new_path = ""
        if (columns.length > 2) {
            new_path = columns[2].split("/")
            new_path = "/" + new_path.slice(1,new_path.length).join("/")
        }
        //console.log(new_path)
        let row = {
            "action": columns[0],
            'hash': columns[1],
            'path': new_path
        }
        if (columns.length > 3) {
            for (let i = 3; i < columns.length; i++) {
                row['column-' + i] = columns[i];
            }
        }        
        ingest_ipfs_rows.push(row);
    }

    // split at 1 million rows
    const max_rows = 1000001;
    const ingest_ipfs_rows_chunks = [];
    let chunk = [];
    if (ingest_ipfs_rows.length <= max_rows) {
        ingest_ipfs_rows_chunks.push(ingest_ipfs_rows);
        fs.writeFileSync(ipfs_output_path.replace(" .tsv","").replace(".tsv","") + '.json', JSON.stringify(ingest_ipfs_rows))
        fs.rmSync(ipfs_output_path);
        return ingest_ipfs_rows_chunks;
    }
    else{
        for (let i = 0; i < ingest_ipfs_rows.length; i++) {
            chunk.push(ingest_ipfs_rows[i]);
            if (chunk.length - 1 % max_rows === 0) {
                const chunkFileName = ipfs_output_path.replace(" .tsv","").replace(".tsv","") + '_chunk_' + Math.floor(i / max_rows) + '_to_'+ i+ '.json';
                let startIndex = Math.floor(i / max_rows) + 1;
                let endIndex = i;
                while (startIndex < endIndex) {
                    const subChunkString = JSON.stringify(ingest_ipfs_rows.slice(startIndex, endIndex));
                    fs.writeFileSync(path.join(chunkFileName), subChunkString);
                    startIndex++;
                    fs.rmSync(ipfs_output_path);
                }
                ingest_ipfs_rows_chunks.push(chunk);
                chunk = [];
            }
    
        }
        return ingest_ipfs_rows_chunks;
    }
    return ingest_ipfs_rows_chunks;
}

export function main(file_path){
    if(fs.existsSync(file_path)){
        if(fs.readdirSync(file_path).length > 0){
            const files = fs.readdirSync(file_path);
            for(const file of files){
                if (file.endsWith(".tsv")){
                    const this_file_path = path.join(file_path, file);
                    const ingest_ipfs_rows_chunks = convert(this_file_path);
                    console.log("number of chunks from file: ${file_path}")
                    console.log(ingest_ipfs_rows_chunks.length);
                }
            }
        }
    }
}

main("./ipfs_pins/")
