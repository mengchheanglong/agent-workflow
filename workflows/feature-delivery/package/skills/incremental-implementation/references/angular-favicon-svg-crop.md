# Angular favicon SVG crop and legibility

Use when a user provides a large-canvas SVG logo for the browser favicon and asks for it to be more visible.

## Pattern

1. Copy the supplied SVG into `public/favicon.svg` rather than linking to the attachment path.
2. Update `src/index.html` to use the SVG favicon:
   ```html
   <link rel="icon" type="image/svg+xml" href="favicon.svg">
   ```
3. Inspect the root `<svg>` tag. Large exported logos often have a full presentation canvas such as `viewBox="0 0 1024.5 576"`, which makes the mark tiny in a browser tab.
4. Crop by editing only the root `viewBox`, preserving the embedded artwork and masks.
   - Start with a square crop around the mark.
   - Tighten until the visible white/logo pixels nearly touch the square edges.
   - For favicon legibility, a crop that leaves only a few pixels of margin at a 512px render is usually better than a visually spacious logo preview.
5. Verify from the app origin, not just a local `file://` preview:
   - Load `/favicon.svg` or the app page.
   - Confirm `document.querySelector('link[rel="icon"]').href` points to `/favicon.svg` and `type` is `image/svg+xml`.
   - Run the canonical Angular check (`pnpm check`).

## Browser-measurement helper

When the favicon is same-origin (for example after loading the app at `http://localhost:4300/`), use a temporary canvas in DevTools/browser console to estimate rendered white/logo margins:

```js
(async()=>{
  const img=new Image();
  img.src='/favicon.svg?bbox='+Date.now();
  await img.decode();
  const size=512,c=document.createElement('canvas');
  c.width=size;c.height=size;
  const ctx=c.getContext('2d');
  ctx.drawImage(img,0,0,size,size);
  const d=ctx.getImageData(0,0,size,size).data;
  let minX=size,minY=size,maxX=-1,maxY=-1,count=0;
  for(let y=0;y<size;y++) for(let x=0;x<size;x++) {
    const i=(y*size+x)*4,r=d[i],g=d[i+1],b=d[i+2],a=d[i+3];
    if(a>0&&r>180&&g>180&&b>180){
      if(x<minX)minX=x;if(x>maxX)maxX=x;
      if(y<minY)minY=y;if(y>maxY)maxY=y;count++;
    }
  }
  return {
    bboxPx:{minX,minY,maxX,maxY,width:maxX-minX+1,height:maxY-minY+1},
    marginsPx:{left:minX,top:minY,right:size-1-maxX,bottom:size-1-maxY},
    count
  };
})()
```

If canvas reads fail on `file://` with a tainted-canvas error, load the app and measure `/favicon.svg` from the same origin.

## Pitfalls

- Do not leave a full presentation canvas around a favicon; it will be too small to recognize.
- Do not stop after the logo “looks nice” in a large preview. The favicon goal is maximum recognizability at tiny tab size.
- If the user asks “bigger until the edge touches the white spot/logo,” interpret that literally: reduce the crop margins to near-edge without clipping important ears/tail/eyes.
- Avoid converting to PNG unless needed; SVG favicons can preserve sharp edges and are easy to crop by viewBox.
